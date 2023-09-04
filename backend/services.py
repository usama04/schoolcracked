from fastapi import Request, HTTPException, status
import aiohttp
import settings
from api.agent import async_agent_executor
from config.database import collection_name
from models.chats_models import Chat
from schemas.chats_schemas import chat_serializer, chats_serializer
from datetime import datetime as dt
import pytz
from typing import Any, Coroutine, List, Optional, Dict
from functools import partial
################# Langchain Built-in conversational Agent imports
from langchain.agents import load_tools, AgentExecutor
from langchain.tools import BaseTool, Tool
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.schema import HumanMessage, AIMessage
from langchain.utilities.wolfram_alpha import WolframAlphaAPIWrapper
from langchain.utilities import WikipediaAPIWrapper
from typing import Optional, Type
from langchain.callbacks.manager import AsyncCallbackManagerForToolRun, CallbackManagerForToolRun
import wolframalpha
from dotenv import load_dotenv
from PIL import Image
from urllib.parse import urlparse, quote_plus
import replicate
import os
import asyncio
import io
import api.convAgent as Conv_Agent

load_dotenv()

############ LLM and tools ###############
llm=ChatOpenAI(temperature=0)
async_tools = load_tools(["serpapi", "pal-math", "llm-math"], llm=llm)
class CustomWolframTool(BaseTool):
    name = "wolfram_tool"
    description = "Queries the Wolfram Alpha API. Useful for when you need to answer questions about Calculus, Algebra and Symbolic math. Input should be a search query."
    client = wolframalpha.Client(settings.WOLFRAM_ALPHA_APPID)

    def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        """Use the tool."""
        wolfram_wrapper = WolframAlphaAPIWrapper()
        return wolfram_wrapper.run(query)
    
    async def _arun(self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        """Use the tool asynchronously."""
        async def querywolf(question):
          res = self.client.query(question)
          return next(res.results).text
        return await querywolf(query)

wolfram = CustomWolframTool()
wolfram_tool = Tool(
    name="Wolfram Alpha",
    description = "Queries the Wolfram Alpha API. Useful for when you need to answer questions about Calculus, Algebra and Symbolic math. Input should be a search query.",
    func=wolfram.run,
    coroutine=wolfram.arun,
)

class CustomImageReaderTool(BaseTool):
    name = "image_reader_tool"
    description = "Generates the description of an image from a prompt provided to it, Provides a list of objects detected if any, and also analyses any text in the image from an OCR if a text is present. \
        The input format to this tool SHOULD BE in the following format: image_path|||prompt message where image_path is the path to the image and prompt is a COMPREHENSIVE AND VERBOSE and should be in English regarding the information required from the image.\
        Output from image reader is always valid. You may summarize the objects detected portion if there are repeated objects.\
        Make sure to give it a very detailed and comprehensive question as prompt.\
        You must analyze the output from this tool and provide a comprehensive and detailed final answer based on your analysis of the output from this tool."
        
    async def image_caption_async(self, image_path_and_prompt):
        """
        Generates text in response to an input image and prompt. Useful for understanding the content of an image.
        """
        image_data = image_path_and_prompt.split("|||")
        image_path = image_data[0]
        prompt = image_data[1]
        is_url = urlparse(image_path).scheme != ""

        try:
            loop = asyncio.get_event_loop()

            def run_replicate():
                if is_url:
                    return replicate.run(settings.IMAGE_TO_TEXT, input={"image": image_path, "prompt": prompt})
                else:
                    with open(image_path, "rb") as image_file:
                        return replicate.run(settings.IMAGE_TO_TEXT, input={"image": image_file, "prompt": prompt})

            repl_output = await loop.run_in_executor(None, run_replicate)

            return repl_output
        
        except Exception as e:
            # print(f"Error executing the image reader tool: {str(e)}")
            return ""
        
    async def aws_image_labels_async(self, image_path):
        is_url = urlparse(image_path).scheme != "" and not os.path.isfile(image_path)
        
        try:
            if not is_url:
                with open(image_path, "rb") as image_file:
                    resized_image_bytes = await self._resize_image(image_file)
                    response = await self._detect_labels_from_bytes(Image={"Bytes": resized_image_bytes})
                    objects = [obj["Name"] for obj in response["Labels"]]
                    return objects
            if is_url:
                async with aiohttp.ClientSession() as session:
                    async with session.get(image_path) as response:
                        image_data = await response.read()
                resized_image_bytes = await self._resize_image(io.BytesIO(image_data))
                response = await self._detect_labels_from_bytes(Image={"Bytes": resized_image_bytes})
                objects = [obj["Name"] for obj in response["Labels"]]
                return objects
        except:
            return [""]
        
    async def _detect_labels_from_bytes(self, **kwargs):
        loop = asyncio.get_running_loop()
        partial_fn = partial(settings.rek_client.detect_labels, **kwargs)
        response = await loop.run_in_executor(None, partial_fn)
        return response
    
    async def aws_OCR_async(self, image_path):
        is_url = urlparse(image_path).scheme != "" and not os.path.isfile(image_path)
        
        try:
            if not is_url:
                with open(image_path, "rb") as image_file:
                    resized_image_bytes = await self._resize_image(image_file)
                    response = await self._detect_text_from_bytes(Image={"Bytes": resized_image_bytes})
                    objects = [obj["DetectedText"] for obj in response["TextDetections"] if obj["Confidence"] > 90]
                    return objects
            if is_url:
                async with aiohttp.ClientSession() as session:
                    async with session.get(image_path) as response:
                        image_data = await response.read()
                resized_image_bytes = await self._resize_image(io.BytesIO(image_data))
                response = await self._detect_text_from_bytes(Image={"Bytes": resized_image_bytes})
                objects = [obj["DetectedText"] for obj in response["TextDetections"] if obj["Confidence"] > 90]
                return objects
        except:
            return [""]
        
    async def _detect_text_from_bytes(self, **kwargs):
        loop = asyncio.get_running_loop()
        partial_fn = partial(settings.rek_client.detect_text, **kwargs)
        response = await loop.run_in_executor(None, partial_fn)
        return response

    async def _resize_image(self, image_data):
        loop = asyncio.get_running_loop()
        img = await loop.run_in_executor(None, Image.open, image_data)

        max_size = (700, 700)
        img.thumbnail(max_size)

        # Save the resized image to a bytes buffer
        output_buffer = io.BytesIO()
        save_image = partial(img.save, output_buffer, format=img.format)
        await loop.run_in_executor(None, save_image)
        return output_buffer.getvalue()
    
    async def image_reader_async(self, image_path_and_prompt):
        """
        Generates the description of an image from a prompt provided to it and also provides the list of objects detected in the image.
        """
        image_path = image_path_and_prompt.split("|||")[0]
        # Gather all the coroutines to execute them in parallel
        description_task = self.image_caption_async(image_path_and_prompt)
        objects_task = self.aws_image_labels_async(image_path)
        characters_task = self.aws_OCR_async(image_path)
        
        # Wait for all the tasks to complete in parallel
        description, objects, characters = await asyncio.gather(description_task, objects_task, characters_task)
        
        return f"Description: {description}\n" + f"Objects: {', '.join(objects)}\n" if objects != [""] else "" + f"OCR Results: {', '.join(characters)}\n" if characters != [""] else ""
    
    async def _arun(self, image_path_and_prompt: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        """Use the tool asynchronously."""
        return await self.image_reader_async(image_path_and_prompt)
    
    def _run(self, image_path_and_prompt: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        """Use the tool."""
        return asyncio.run(self.image_reader_async(image_path_and_prompt))

image_reader = CustomImageReaderTool()
image_reader_tool = Tool(
    name="Image Reader",
    description="Generates the description of an image from a prompt provided to it, Provides a list of objects detected if any, and also analyses any text in the image from an OCR if a text is present. \
        The input format to this tool SHOULD BE in the following format: image_path|||prompt message where image_path is the path to the image and prompt is a COMPREHENSIVE AND VERBOSE and should be in English regarding the information required from the image.\
        Output from image reader is always valid. You may summarize the objects detected portion if there are repeated objects.\
        Make sure to give it a very detailed and comprehensive question as prompt.\
        You must analyze the output from this tool and provide a comprehensive and detailed final answer based on your analysis of the output from this tool.",
    func=image_reader.run,
    coroutine=image_reader.arun,
)

async_tools.extend([wolfram_tool, image_reader_tool])

###########################################


async def create_chat(user_id: int, prompt: Dict[str, str], generated: Dict[str, str]) -> dict:
    chat = {"user_id": user_id, "prompt": prompt, "generated": generated, "created_at": dt.now(tz=pytz.UTC)}
    result = collection_name.insert_one(chat)
    chat["_id"] = str(result.inserted_id)
    response = chat_serializer(chat)
    return {"status": "ok", "data": response}

async def assistantChat(request: Request):
    header = request.headers
    if "Authorization" not in header:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")
    token = header["Authorization"].split("Bearer ")[1]
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    # Make request to AUTH_BACKEND_URL to validate token using aiohttp to /auth/jwt/verify with a post request
    async with aiohttp.ClientSession() as session:
        async with session.post(settings.AUTH_BACKEND_URL + "/auth/jwt/verify/", json={"token": token}) as response:
            if response.status != 200:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
            else:
                # get user information from /auth/users/me
                async with session.get(settings.AUTH_BACKEND_URL + "/auth/users/me/", headers={"Authorization": "JWT " + token}) as user_response:
                    user = await user_response.json()
    try:
        recieved = await request.json()
        messages = recieved["messages"]
        prompt = "\n"
        for message in messages:
            if message["role"] == "questioner":
                try:
                    mes = message["message"]
                except KeyError:
                    mes = message["content"]
                except:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid message format")
                prompt += "Questioner: " + mes + "\n"
            else:
                try:
                    mes = message["message"]
                except KeyError:
                    mes = message["content"]
                except:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid message format")
                prompt += "Assistant: " + mes + "\n"
        #agent_output = agent_executor.run(prompt)
        #agent_output = await agent_executor.arun(prompt)
        agent_output = await async_agent_executor(prompt)
        if "Assistant:" in agent_output[:8]:
            agent_output = agent_output.split("Assistant: ")[1]
        ret_response = {"user": "assistant", "message": agent_output}
        # Save chat to database
        try:
            chat = await create_chat(user["id"], messages, ret_response)
        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An error occured while processing the request")
        return ret_response
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An error occured while processing the request")
    
    
############## Langchain Built-in conversation Agent #################
    
async def agentChat(request: Request):
    header = request.headers
    if "Authorization" not in header:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")
    token = header["Authorization"].split("Bearer ")[1]
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    # Make request to AUTH_BACKEND_URL to validate token using aiohttp to /auth/jwt/verify with a post request
    async with aiohttp.ClientSession() as session:
        async with session.post(settings.AUTH_BACKEND_URL + "/auth/jwt/verify/", json={"token": token}) as response:
            if response.status != 200:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
            else:
                # get user information from /auth/users/me
                async with session.get(settings.AUTH_BACKEND_URL + "/auth/users/me/", headers={"Authorization": "JWT " + token}) as user_response:
                    user = await user_response.json()
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    try:
        recieved = await request.json()
        messages = recieved["messages"][:-1]
        for message in messages:
            if message["role"] == "questioner":
                try:
                    mes = message["message"]
                except KeyError:
                    mes = message["content"]
                except:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid message format")
                memory.buffer.append(HumanMessage(content=mes))
            else:
                try:
                    mes = message["message"]
                except KeyError:
                    mes = message["content"]
                except:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid message format")
                memory.buffer.append(AIMessage(content=mes))
        # print("Memory: ", memory.buffer)
        try:
            prompt = recieved["messages"][-1]["message"]
        except KeyError:
            prompt = recieved["messages"][-1]["content"]
        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid message format")
        agent_chain = initialize_agent(async_tools, llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, verbose=False, memory=memory)
        agent_output = await agent_chain.arun(prompt)
        # print("Agent output: ", agent_output)
        if agent_output:
            ret_response = {"user": "assistant", "message": agent_output}
             # Save chat to database
            try:
                chat = await create_chat(user["id"], recieved["messages"], ret_response)
                # print("Chat saved", chat)
            except:
                # print("Error saving chat")
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An error occured while processing the request")
        else:
            ret_response = {"user": "assistant", "message": "I don't know what to say"}
        memory.clear()
        return ret_response
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An error occured while processing the request")
    
############################################

############ Custom Conversation Agent #####################

async def customAgentChat(request: Request):
    header = request.headers
    if "Authorization" not in header:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")
    token = header["Authorization"].split("Bearer ")[1]
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    # Make request to AUTH_BACKEND_URL to validate token using aiohttp to /auth/jwt/verify with a post request
    async with aiohttp.ClientSession() as session:
        async with session.post(settings.AUTH_BACKEND_URL + "/auth/jwt/verify/", json={"token": token}) as response:
            if response.status != 200:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
            else:
                # get user information from /auth/users/me
                async with session.get(settings.AUTH_BACKEND_URL + "/auth/users/me/", headers={"Authorization": "JWT " + token}) as user_response:
                    user = await user_response.json()
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    try:
        recieved = await request.json()
        messages = recieved["messages"][:-1]
        for message in messages:
            if message["role"] == "questioner":
                try:
                    mes = message["message"]
                except KeyError:
                    mes = message["content"]
                except:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid message format")
                memory.buffer.append(HumanMessage(content=mes))
            else:
                try:
                    mes = message["message"]
                except KeyError:
                    mes = message["content"]
                except:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid message format")
                memory.buffer.append(AIMessage(content=mes))
        try:
            prompt = recieved["messages"][-1]["message"]
        except KeyError:
            prompt = recieved["messages"][-1]["content"]
        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid message format")
        agent = Conv_Agent.AITeachingAssistant.from_llm_and_tools(llm=llm, tools=async_tools, memory=memory, verbose=False)
        agent_executor = AgentExecutor(agent=agent, tools=async_tools, memory=memory, verbose=False)
        agent_output = await agent_executor.arun(input=prompt)
        if agent_output:
            ret_response = {"user": "assistant", "message": agent_output}
             # Save chat to database
            try:
                chat = await create_chat(user["id"], recieved["messages"], ret_response)
                # print("Chat saved", chat)
            except:
                # print("Error saving chat")
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An error occured while processing the request")
        else:
            ret_response = {"user": "assistant", "message": "I don't know what to say"}
        memory.clear()
        return ret_response
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An error occured while processing the request")