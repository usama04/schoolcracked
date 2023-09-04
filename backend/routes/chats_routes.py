from fastapi import APIRouter
from config.database import collection_name
from models.chats_models import Chat
from schemas.chats_schemas import chat_serializer, chats_serializer
from bson import ObjectId
from datetime import datetime as dt
from typing import List, Optional, Dict
import pytz

chats_api_router = APIRouter()

@chats_api_router.get("/api/chats/{user_id}")
async def chats(user_id: int):
    chats = collection_name.find({"user_id": user_id})
    response = chats_serializer(chats, user_id)
    return response

@chats_api_router.get("/api/chats/{user_id}/{chat_id}")
async def chat(user_id: int, chat_id: str):
    chat = collection_name.find_one({"_id": ObjectId(chat_id)})
    if chat["user_id"] != user_id:
        return {"status": "error", "message": "Unauthorized"}
    response = chat_serializer(chat)
    return response

@chats_api_router.post("/api/chats/{user_id}")
async def create_chat(user_id: int, prompt: List[Dict[str, str]], generated: Dict[str, str]) -> dict:
    chat = {"user_id": user_id, "prompt": prompt, "generated": generated, "created_at": dt.now(tz=pytz.UTC)}
    result = collection_name.insert_one(chat)
    chat["_id"] = str(result.inserted_id)
    response = chat_serializer(chat)
    return response

@chats_api_router.delete("/api/chats/{user_id}/{chat_id}")
async def delete_chat(user_id: int, chat_id: str):
    chat = collection_name.find_one({"_id": ObjectId(chat_id)})
    if chat["user_id"] != user_id:
        return {"status": "error", "message": "Unauthorized"}
    collection_name.delete_one({"_id": ObjectId(chat_id)})
    return {"status": "success", "message": "Chat deleted"}