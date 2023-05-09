from typing import List, Optional, Dict
import datetime as dt
import pydantic as pyd

class UserBase(pyd.BaseModel):
    email: str
    scholar: bool = False
    
class UserCreate(UserBase):
    first_name: str
    last_name: str
    bio: str
    location: str
    hashed_password: str
    confirm_password: str
    
    class Config:
        orm_mode = True
        
class User(UserBase):
    id: int
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    
    class Config:
        orm_mode = True
        
class UserUpdate(UserBase):
    id: int = None
    
class EmailSchema(pyd.BaseModel):
    email: pyd.EmailStr
        
class ResetPassword(pyd.BaseModel):
    password: str
    confirm_password: str
    
class ChangePassword(pyd.BaseModel):
    old_password: str
    new_password: str
    confirm_password: str   

class ProfileBase(pyd.BaseModel):
    first_name: str = None
    last_name: str = None
    bio: str = None
    location: str = None
    birth_date: dt.date = None
    
class ProfileCreate(ProfileBase):
    profile_image: str = None

class Profile(ProfileBase):
    profile_image: str = None
    created_at: dt.datetime
    updated_at: dt.datetime
    
    class Config:
        orm_mode = True
        
class ProfileUpdate(ProfileBase):
    user_id: int = None

class UserProfileResponse(pyd.BaseModel):
    user: User
    profile: Profile
    
    class Config:
        orm_mode = True
        
class ChatsBase(pyd.BaseModel):
    user_id: int
    prompt: List[Dict[str, str]]
    generated_response: Dict[str, str]
    tokens_used: int = 0

class ChatsCreate(ChatsBase):
    pass

class Chats(ChatsBase):
    id: int
    created_at: Optional[str] = None

    class Config:
        orm_mode = True
        
class AltChatResponse(pyd.BaseModel):
    response_rating: int = None
    alt_response: str = None