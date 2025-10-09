from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ChatSessionCreate(BaseModel):
    """创建会话"""
    title: Optional[str] = "新对话"


class ChatSessionResponse(BaseModel):
    """会话响应"""
    id: int
    user_id: int
    title: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ChatMessageCreate(BaseModel):
    """创建消息"""
    session_id: int
    content: str


class ChatMessageResponse(BaseModel):
    """消息响应"""
    id: int
    session_id: int
    role: str
    content: str
    tokens_used: int
    model: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class ChatHistoryResponse(BaseModel):
    """对话历史响应"""
    session: ChatSessionResponse
    messages: List[ChatMessageResponse]

