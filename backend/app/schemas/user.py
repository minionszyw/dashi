from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal


class UserLogin(BaseModel):
    """微信登录请求"""
    code: str


class UserCreate(BaseModel):
    """创建用户"""
    openid: str
    unionid: Optional[str] = None
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None


class UserResponse(BaseModel):
    """用户响应"""
    id: int
    openid: str
    nickname: Optional[str]
    avatar_url: Optional[str]
    token_balance: Decimal
    created_at: datetime
    last_login_at: Optional[datetime]

    class Config:
        from_attributes = True


class UserStats(BaseModel):
    """用户统计"""
    total_sessions: int
    total_messages: int
    total_tokens_used: int
    total_spent: Decimal

