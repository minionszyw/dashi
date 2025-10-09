from typing import Optional, Any
from pydantic import BaseModel
from datetime import datetime


class ResponseModel(BaseModel):
    """统一响应模型"""
    code: int = 0
    message: str = "success"
    data: Optional[Any] = None
    timestamp: int = int(datetime.now().timestamp())

