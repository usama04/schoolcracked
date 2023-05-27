from typing import List, Optional, Dict
from pydantic import BaseModel
from datetime import datetime

class Chat(BaseModel):
    _id: str
    user_id: int
    prompt: List[Dict[str, str]]
    generated: Dict[str, str]
    created_at: datetime