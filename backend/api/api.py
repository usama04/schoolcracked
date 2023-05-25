import os

import databases.models as models
import databases.schemas as schemas
import fastapi.security as security
import openai
import passlib.hash as ph
import services as services
import settings
import sqlalchemy.orm as orm
from api.responses import CustomJSONResponse
from fastapi import (Depends, FastAPI, File, Form, HTTPException, Request,
                     UploadFile, WebSocket, status, WebSocketDisconnect, Header)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

openai.api_key = settings.OPENAI_API_KEY

app = FastAPI(
    default_response_class=CustomJSONResponse,
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/api")
async def root():
    return {"message": "Check docs for more info."}


### CHATBOT ###

@app.get("/api/chat-history")
async def get_chat_history(db: orm.Session = Depends(services.get_db), user: schemas.User = Depends(services.get_current_user)):
    return await services.get_chat_history(db, user)

@app.get("/api/chat-history/{chat_id}")
async def get_chat_history_by_id(chat_id: int, db: orm.Session = Depends(services.get_db), user: schemas.User = Depends(services.get_current_user)):
    return await services.get_chat_history_by_id(db, user, chat_id)

@app.delete("/api/chat-history/{chat_id}")
async def delete_chat_history_by_id(chat_id: int, db: orm.Session = Depends(services.get_db), user: schemas.User = Depends(services.get_current_user)):
    return await services.delete_chat_history_by_id(db, user, chat_id)

@app.post("/api/chatbot")
async def agentChat(request: Request, db: orm.Session = Depends(services.get_db), user: schemas.User = Depends(services.get_current_user)):
    return await services.agent(request, db, user)
        
@app.post("/api/assistant")
async def assistantChat(request: Request):
    return await services.assistantChat(request)
