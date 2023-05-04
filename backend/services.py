from fastapi import Depends, HTTPException, UploadFile, File, Request, status
import fastapi.security as security
from databases import database as db
import sqlalchemy.orm as orm
import databases.models as models
import databases.schemas as schemas
import passlib.hash as ph
import datetime as dt
import jwt
import settings
from typing import List, Dict
from fastapi_mail import FastMail, MessageSchema, MessageType
import openai
from api.agent import async_agent_executor
openai.api_key = settings.OPENAI_API_KEY

def create_database():
    return db.Base.metadata.create_all(bind=db.engine)

def get_db():
    db_session = db.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
        
async def get_user_by_email(db: orm.Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

async def create_user(db: orm.Session, user: schemas.UserCreate):
    password = user.hashed_password
    confirm_password = user.confirm_password
    if user.email is None:
        raise HTTPException(status_code=400, detail='Email is required')
    if await get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=400, detail='Email already registered')
    if password is None:
        raise HTTPException(status_code=400, detail='Password is required')
    if password != confirm_password:
        raise HTTPException(status_code=400, detail='Passwords do not match')
    db_user = models.User(email=user.email, hashed_password=ph.bcrypt.hash(password), scholar=user.scholar)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

async def create_user_profile(db: orm.Session, profile: schemas.ProfileCreate, user_id: int, first_name: str, last_name: str, bio: str, location: str):
    db_profile = models.Profile(
        first_name=first_name,
        last_name=last_name,
        bio=bio, 
        location=location, 
        birth_date=profile.birth_date, 
        profile_image=profile.profile_image, user_id=user_id)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

async def authenticate_user(db: orm.Session, email: str, password: str):
    user = await get_user_by_email(db, email=email)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user

async def create_token(db: orm.Session, user: models.User):
    user_obj = schemas.User.from_orm(user)
    if user_obj.is_active == False:
        raise HTTPException(status_code=401, detail='User is not active')
    expiry = dt.datetime.utcnow() + dt.timedelta(minutes=settings.JWT_TOKEN_EXPIRE_MINUTES)
    payload = {"user": user_obj.dict(), "exp": expiry}
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return dict(access_token=token, token_type='bearer')

async def get_current_user(db: orm.Session = Depends(get_db), token: str = Depends(settings.OAUTH2_SCHEME)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        if dt.datetime.fromtimestamp(payload.get('exp')) < dt.datetime.utcnow():
            raise HTTPException(status_code=401, detail='Invalid Credentials')
        else:
            user = db.query(models.User).get(payload.get('user')["id"])
    except:
        raise HTTPException(status_code=401, detail='Invalid Credentials')
    return schemas.User.from_orm(user)

async def verify_token(db: orm.Session = Depends(get_db), user: schemas.User = Depends(get_current_user)):
    if user:
        return dict(message='Token is valid')
    else:
        raise HTTPException(status_code=401, detail='Invalid Credentials')

async def logout(db: orm.Session, user: schemas.User = Depends(get_current_user)):
    return dict(message='Logged out successfully')

async def update_user(db: orm.Session = Depends(get_db), user: schemas.UserUpdate = Depends(get_current_user)):
    #update existing user
    db_user = db.query(models.User).get(user.id)
    db_user.email = user.email
    db_user.first_name = user.first_name
    db_user.last_name = user.last_name
    db.commit()
    db.refresh(db_user)
    return db_user

async def send_email(to_email, subject, body):
    message = MessageSchema(
        subject=subject,
        recipients=[to_email],
        body=body,
        subtype=MessageType.html
    )
    fm = FastMail(settings.EMAIL_CONFIG)
    try:
        await fm.send_message(message)
        return dict(message='Email sent successfully')
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Email could not be sent')

async def forgot_password(db: orm.Session, email: str):
    user = await get_user_by_email(db, email=email)
    if user:
        profile = db.query(models.Profile).filter(models.Profile.user_id == user.id).first()
        payload = {"user": user.id, "exp": dt.datetime.utcnow() + dt.timedelta(minutes=settings.JWT_TOKEN_EXPIRE_EMAIL_MINUTES)}
        profile = db.query(models.Profile).filter(models.Profile.user_id == user.id).first()
        token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
        reset_link = f'{settings.FRONTEND_URL}/reset-password/{token}'
        subject = 'Password Reset Request'
        body = f'<p>Hi {profile.first_name},\n\nYou have requested to reset your password. Please click the link below to reset your password.\n\n{reset_link}\n\nIf you did not make this request, please ignore this email.</p>'
        await send_email(email, subject, body)
        return dict(message='Password reset link sent to your email')
    else:
        raise HTTPException(status_code=400, detail='Email not registered')
    
async def reset_password(db: orm.Session, token: str, password: str, confirm_password: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        user = db.query(models.User).get(payload.get('user'))
        if not user:
            raise HTTPException(status_code=400, detail='Invalid token')
        
        if dt.datetime.fromtimestamp(payload.get('exp')) < dt.datetime.utcnow():
            raise HTTPException(status_code=400, detail='Token expired')
        
        if password != confirm_password:
            raise HTTPException(status_code=400, detail='Passwords do not match')
        
        user.set_password(password)
        db.commit()
        db.refresh(user)
        return dict(message='Password reset successfully')
    except:
        raise HTTPException(status_code=400, detail='Invalid token')
    
async def change_password(db: orm.Session = Depends(get_db), user: schemas.User = Depends(get_current_user), change_password: schemas.ChangePassword = Depends()):
    user_obj = db.query(models.User).get(user.id)
    if not user_obj.verify_password(change_password.old_password):
        raise HTTPException(status_code=400, detail='Current password is incorrect')
    if change_password.new_password != change_password.confirm_password:
        raise HTTPException(status_code=400, detail='Passwords do not match')
    if change_password.old_password == change_password.new_password:
        raise HTTPException(status_code=400, detail='New password cannot be same as current password')
    user_obj.set_password(change_password.new_password)
    db.commit()
    db.refresh(user_obj)
    return dict(message='Password changed successfully')

async def send_verification_email(db: orm.Session = Depends(get_db), user: schemas.User = Depends(get_current_user)):
    user_obj = db.query(models.User).get(user.id)
    profile_obj = db.query(models.Profile).filter(models.Profile.user_id == user_obj.id).first()
    if user_obj.is_active:
        raise HTTPException(status_code=400, detail='Email already verified')
    payload = {"user": user_obj.id, "exp": dt.datetime.utcnow() + dt.timedelta(minutes=settings.JWT_TOKEN_EXPIRE_EMAIL_MINUTES)}
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    verify_link = f'{settings.FRONTEND_URL}/verify-email/{token}'
    subject = 'Email Verification'
    body = f'<p>Hi {profile_obj.first_name},\n\nPlease click the link below to verify your email.\n\n{verify_link}\n\nIf you did not make this request, please ignore this email.</p>'
    await send_email(user_obj.email, subject, body)
    return dict(message='Verification link sent to your email')

async def verify_email(db: orm.Session, token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        user = db.query(models.User).get(payload.get('user'))
        if not user:
            raise HTTPException(status_code=400, detail='Invalid token')
        
        if dt.datetime.fromtimestamp(payload.get('exp')) < dt.datetime.utcnow():
            raise HTTPException(status_code=400, detail='Token expired')
        
        if user.scholar == True:
            mail = "Welcome to AalimGPT, your email has been verified successfully. Since you selected Scholar, Scholars are in the driving seat of this project and have extra priviledges on our platform. We will therefore, contact you shortly and verify your credentials and manually activate your account before you can start using our services."
            subject = "Email Verification Successful"
            await send_email(user.email, subject, mail)
            user.is_active = False
            await send_email(settings.ADMIN_EMAIL, "New Scholar Registered", f"New Scholar {user.email} and id {user.id} has registered. Please verify their credentials.")
        else:
            user.is_active = True
        
        db.commit()
        db.refresh(user)
        return dict(message='Email verified successfully')
    except:
        raise HTTPException(status_code=400, detail='Invalid token')

async def delete_user(db: orm.Session = Depends(get_db), user: schemas.User = Depends(get_current_user)):
    user_obj = db.query(models.User).get(user.id)
    try:
        await delete_all_chats(db, user_obj)
        await delete_profile(db, user_obj)
        db.delete(user_obj)
        db.commit()
        db.refresh(user_obj)
        return dict(message='User deleted successfully')
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='User could not be deleted')

async def get_profile_by_user_id(db: orm.Session = Depends(get_db), user: int = Depends(get_current_user)):
    return db.query(models.Profile).filter(models.Profile.user_id == user.id).first()

async def update_profile(db: orm.Session = Depends(get_db), profile: schemas.ProfileUpdate = Depends(get_profile_by_user_id), user: schemas.User = Depends(get_current_user)):
    db_profile = db.query(models.Profile).filter(models.Profile.user_id == user.id).first()
    try:
        db_profile.first_name = profile.first_name
        db_profile.last_name = profile.last_name
        db_profile.bio = profile.bio
        db_profile.location = profile.location
        db_profile.birth_date = profile.birth_date
        db.commit()
        db.refresh(db_profile)
    except Exception as e:
        print(e)
    return db_profile

async def update_profile_image(db: orm.Session = Depends(get_db), user: schemas.User = Depends(get_current_user), file: UploadFile = File(...)):
    s3_client = settings.s3_client
    db_profile = db.query(models.Profile).filter(models.Profile.user_id == user.id).first()
    if file:
        file_key = f'profile_images/{user.id}/{file.filename}'
        try:
            s3_client.upload_fileobj(file.file, settings.S3_BUCKET_NAME, file_key)
            db_profile.profile_image = f'https://{settings.S3_BUCKET_NAME}.s3.amazonaws.com/profile_images/{user.id}/{file.filename}'
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail='Error uploading file')
    db.commit()
    db.refresh(db_profile)
    return db_profile

async def delete_profile(db: orm.Session = Depends(get_db), user: schemas.User = Depends(get_current_user)):
    profile_obj = db.query(models.Profile).filter(models.Profile.user_id == user.id).first()
    db.delete(profile_obj)
    db.commit()
    return dict(message='Profile deleted successfully')

async def save_chat_response(db: orm.Session = Depends(get_db), user: schemas.User = Depends(get_current_user), prompt: List[Dict[str, str]] = None, generated_response: Dict[str, str] = None):
    chat = models.Chats(user_id=user.id)
    chat.set_prompt(prompt)
    chat.set_generated_response(generated_response)
    chat.count_tokens()
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat


async def get_chat_history(db: orm.Session = Depends(get_db), user: schemas.User = Depends(get_current_user)):
    return db.query(models.Chats).filter(models.Chats.user_id == user.id).all()

async def get_chat_history_by_id(db: orm.Session = Depends(get_db), user: schemas.User = Depends(get_current_user), chat_id: int = None):
    return db.query(models.Chats).filter(models.Chats.user_id == user.id, models.Chats.id == chat_id).first()

async def delete_chat_history_by_id(db: orm.Session = Depends(get_db), user: schemas.User = Depends(get_current_user), chat_id: int = None):
    db.query(models.Chats).filter(models.Chats.user_id == user.id, models.Chats.id == chat_id).delete()
    db.commit()
    return dict(message='Chat history deleted successfully')

async def delete_all_chats(db: orm.Session = Depends(get_db), user: schemas.User = Depends(get_current_user)):
    db.query(models.Chats).filter(models.Chats.user_id == user.id).delete()
    db.commit()
    return dict(message='All chat history deleted successfully')

async def provide_alternate_answer(db: orm.Session = Depends(get_db), user: schemas.User = Depends(get_current_user), chat_id: int = None, alternate_answer: Dict[str, str] = None):
    rating = alternate_answer.response_rating
    alt_answer = alternate_answer.alt_response
    chat_obj = db.query(models.Chats).filter(models.Chats.user_id == user.id, models.Chats.id == chat_id).first()
    chat_obj.response_rating = rating
    chat_obj.alt_response = alt_answer
    db.commit()
    db.refresh(chat_obj)
    return dict(message='Alternate answer provided successfully', answer=chat_obj.alt_response)
    
    
async def mufti_gpt3(request: Request, db: orm.Session = Depends(get_db), user: schemas.User = Depends(get_current_user)):
    received = await request.json()
    #print(received)
    messages = received["messages"]
    #print(messages)
    prompt = "You are a well versed Islamic Scholar who can be asked questions from and he can give answers according to Quran and Hadees with proper references with international numbering of the books of Ahadis. Respond in language question was asked in. Make sure all answers have evidence with it from Quran and Hadees. Be as verbose as possible.\n\n"
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
            prompt += "Scholar: " + mes + "\n"
    #print(prompt)
    response = openai.Completion.create(
        engine=settings.OPENAI_CHAT_MODEL,
        prompt=prompt + "\nScholar:",
        temperature=0.5,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6
    )
    ret_response = {"user": "assistant", "message": response.choices[0].text}
    chat = await save_chat_response(db, user, prompt=messages, generated_response=ret_response)
    ret_response["chat_id"] = chat.id
    return ret_response   
    
async def mufti_agent(request: Request, db: orm.Session = Depends(get_db), user: schemas.User = Depends(get_current_user)):
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
            prompt += "Scholar: " + mes + "\n"
    #agent_output = agent_executor.run(prompt)
    #agent_output = await agent_executor.arun(prompt)
    agent_output = await async_agent_executor(prompt)
    if "Scholar:" in agent_output[:8]:
        agent_output = agent_output.split("Scholar: ")[1]
    ret_response = {"user": "assistant", "message": agent_output}
    chat = await save_chat_response(db, user, prompt=messages, generated_response=ret_response)
    ret_response["chat_id"] = chat.id
    return ret_response