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
                     UploadFile, WebSocket, status, WebSocketDisconnect)
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

### AUTHENTICATION ###

@app.post("/api/register")
async def create_user(user: schemas.UserCreate, db: orm.Session = Depends(services.get_db)):
    db_user = await services.get_user_by_email(db, email=user.email)
    if db_user and db_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    if db_user and not db_user.is_active:
        return await services.send_verification_email(db, db_user)
    user_obj = await services.create_user(db, user)
    profile_obj = await services.create_user_profile(db, schemas.ProfileCreate(), user_obj.id, first_name=user.first_name, last_name=user.last_name, bio=user.bio, location=user.location)
    return await services.send_verification_email(db, user_obj)
    #return await services.create_token(db, user_obj)
    
@app.get("/api/verify-email/{token}")
async def verify_email(token, db: orm.Session = Depends(services.get_db)):
    return await services.verify_email(db, token)

@app.post("/api/login")
async def generate_token(form_data: security.OAuth2PasswordRequestForm = Depends(), db: orm.Session = Depends(services.get_db)):
    user = await services.authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    return await services.create_token(db, user)

@app.post("/api/logout")
async def logout(db: orm.Session = Depends(services.get_db), user: schemas.User = Depends(services.get_current_user)):
    return await services.logout(db, user)

@app.get("/api/users/me", response_model=schemas.User)
async def get_user(user: schemas.User = Depends(services.get_current_user)):
    return user

@app.put("/api/users/me", response_model=schemas.User)
async def update_user(user: schemas.UserUpdate, db: orm.Session = Depends(services.get_db)):
    return await services.update_user(db, user)

@app.post("/api/users/reset-password/{token}")
async def reset_password(token, reset_request: schemas.ResetPassword, db: orm.Session = Depends(services.get_db)):
    password = reset_request.password
    confirm_password = reset_request.confirm_password
    return await services.reset_password(db, token, password, confirm_password)

@app.post("/api/users/forgot-password")
async def forgot_password(email: schemas.EmailSchema, db: orm.Session = Depends(services.get_db)):
    email_id = email.email
    return await services.forgot_password(db, email_id)

@app.post("/api/users/change-password")
async def change_password(change_request: schemas.ChangePassword, db: orm.Session = Depends(services.get_db), user: schemas.User = Depends(services.get_current_user)):
    return await services.change_password(db, user, change_request)

@app.delete("/api/users/me")
async def delete_user(db: orm.Session = Depends(services.get_db), user: schemas.User = Depends(services.get_current_user)):
    return await services.delete_user(db, user)

### USER PROFILE ###

@app.get("/api/profile/me")
async def get_profile(db: orm.Session = Depends(services.get_db), user: schemas.User = Depends(services.get_current_user)):
    try:
        return await services.get_profile_by_user_id(db, user=user)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed to get profile.")

@app.put("/api/profile/me", response_model=schemas.Profile)
async def update_profile(profile: schemas.ProfileUpdate, db: orm.Session = Depends(services.get_db), user: schemas.User = Depends(services.get_current_user)):
    return await services.update_profile(db, profile, user)

@app.post("/api/profile/me/upload-image")
async def upload_image(file: UploadFile = File(...), db: orm.Session = Depends(services.get_db), user: schemas.User = Depends(services.get_current_user)):
    return await services.update_profile_image(db, user, file)

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

@app.put("/api/chat-history/{chat_id}")
async def provide_alternate_answer(chat_id: int, alternate_answer: schemas.AltChatResponse, db: orm.Session = Depends(services.get_db), user: schemas.User = Depends(services.get_current_user)):
    return await services.provide_alternate_answer(db, user, chat_id, alternate_answer)

@app.post("/api/chatbot")
async def agentChat(request: Request, db: orm.Session = Depends(services.get_db), user: schemas.User = Depends(services.get_current_user)):
    return await services.agent(request, db, user)
        
