from pydantic import (
    BaseModel, ConfigDict, Field, 
)
from datetime import datetime
from typing import List

class BodyChatsModel(BaseModel):
    title: str = Field(min_length=1, max_length=200)

class BodyTextMessageModel(BaseModel):
    text: str = Field(min_length=1, max_length=5000)

class CountMessageModel(BaseModel):
    count: int = Field(20, ge=1, le=100)

class MessageSchema(BaseModel):
    id: int
    text: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ChatMessageResponse(BaseModel):
    id: int
    title: str
    messages: List[MessageSchema] # Вложенный список сообщений
    model_config = ConfigDict(from_attributes=True)
