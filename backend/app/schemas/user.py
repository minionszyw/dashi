"""
用户相关的Pydantic模型
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID


class UserBase(BaseModel):
    """用户基础模型"""
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None
    gender: Optional[str] = None
    birth_info: Optional[dict] = None


class UserCreate(UserBase):
    """创建用户"""
    openid: str = Field(..., description="微信openid")


class UserUpdate(UserBase):
    """更新用户"""
    pass


class UserResponse(UserBase):
    """用户响应模型"""
    id: UUID
    openid: str
    token_balance: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserSettings(BaseModel):
    """用户设置"""
    context_size: int = Field(default=10, ge=5, le=50, description="上下文消息数")
    ai_style: str = Field(default="professional", description="AI风格")
    stream_output: bool = Field(default=True, description="流式输出")

