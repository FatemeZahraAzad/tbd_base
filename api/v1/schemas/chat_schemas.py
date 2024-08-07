from pydantic import BaseModel
from datetime import datetime

class ChatMessage(BaseModel):
    id: int
    user_id: int
    content: str
    created_at: datetime

    class Config:
        orm_mode = True

class CreateChatMessage(BaseModel):
    content: str