from fastapi import Request, HTTPException, status
import aiohttp
import settings
from api.agent import async_agent_executor
from config.database import collection_name
from models.chats_models import Chat
from schemas.chats_schemas import chat_serializer, chats_serializer
from datetime import datetime as dt
import pytz
from typing import List, Optional, Dict

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

async_tools.append(wolfram_tool)

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