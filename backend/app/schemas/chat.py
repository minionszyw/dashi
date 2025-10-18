"""
对话相关的Pydantic模型
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID


class ConversationCreate(BaseModel):
    """创建会话"""
    title: Optional[str] = Field(default="新会话", max_length=100)
    bazi_profile_id: Optional[UUID] = None
    context_size: int = Field(default=10, ge=5, le=50)
    ai_style: str = Field(default="professional")


class ConversationUpdate(BaseModel):
    """更新会话"""
    title: Optional[str] = Field(None, max_length=100)
    context_size: Optional[int] = Field(None, ge=5, le=50)
    ai_style: Optional[str] = None


class ConversationResponse(BaseModel):
    """会话响应"""
    id: UUID
    user_id: UUID
    title: str
    bazi_profile_id: Optional[UUID]
    context_size: int
    ai_style: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class MessageCreate(BaseModel):
    """发送消息"""
    conversation_id: UUID
    content: str = Field(..., min_length=1, max_length=2000)


class MessageResponse(BaseModel):
    """消息响应"""
    id: UUID
    conversation_id: UUID
    role: str
    content: str
    token_cost: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ChatHistoryResponse(BaseModel):
    """会话历史响应"""
    conversation: ConversationResponse
    messages: List[MessageResponse]
    total: int

