"""
认证相关的Pydantic模型
"""
from pydantic import BaseModel, Field


class WxLoginRequest(BaseModel):
    """微信登录请求"""
    code: str = Field(..., description="微信登录code")


class TokenResponse(BaseModel):
    """Token响应"""
    access_token: str
    token_type: str = "bearer"


class WxLoginResponse(BaseModel):
    """微信登录响应"""
    token: str
    user: dict
    is_new_user: bool = Field(default=False, description="是否新用户")

