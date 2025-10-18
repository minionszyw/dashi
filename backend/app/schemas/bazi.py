"""
八字相关的Pydantic模型
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID


class BaziCalculateRequest(BaseModel):
    """八字计算请求"""
    name: str = Field(..., max_length=50, description="姓名")
    gender: str = Field(..., description="性别（男/女）")
    calendar: str = Field(..., description="日历类型（公历/农历）")
    year: int = Field(..., ge=1900, le=2100, description="年")
    month: int = Field(..., ge=1, le=12, description="月")
    day: int = Field(..., ge=1, le=31, description="日")
    hour: int = Field(..., ge=0, le=23, description="时")
    minute: int = Field(..., ge=0, le=59, description="分")
    birth_city: str = Field(..., description="出生城市")
    current_city: Optional[str] = Field(None, description="现居城市")


class BaziProfileResponse(BaseModel):
    """八字档案响应"""
    id: UUID
    user_id: UUID
    name: str
    gender: str
    birth_info: dict
    bazi_result: dict
    created_at: datetime
    
    class Config:
        from_attributes = True

