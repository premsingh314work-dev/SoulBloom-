from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Request schema for sending a chat message
class ChatRequest(BaseModel):
    message: str

# Single message in chat history
class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime

# Response schema for sending bot reply
class ChatResponse(BaseModel):
    reply: str
    session_id: str

# Response schema for full chat history
class ChatHistoryResponse(BaseModel):
    messages: List[Message]