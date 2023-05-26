from pydantic import BaseModel
from datetime import datetime

class Chat(BaseModel):
    _id: str
    user_id: int
    prompt: str
    generated: str
    created_at: datetime