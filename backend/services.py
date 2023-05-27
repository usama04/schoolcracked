from fastapi import Request, HTTPException, status
import aiohttp
import settings
import openai
from api.agent import async_agent_executor
from config.database import collection_name
from models.chats_models import Chat
from schemas.chats_schemas import chat_serializer, chats_serializer
from datetime import datetime as dt
import pytz
from typing import List, Optional, Dict

openai.api_key = settings.OPENAI_API_KEY


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
                    user = user["data"]
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