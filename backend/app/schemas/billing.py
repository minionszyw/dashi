from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal


class TransactionResponse(BaseModel):
    """交易记录响应"""
    id: int
    user_id: int
    type: str
    amount: Decimal
    balance_after: Optional[Decimal]
    description: Optional[str]
    reference_id: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class RechargeRequest(BaseModel):
    """充值请求"""
    amount: Decimal
    payment_method: str = "wechat"


class RechargeResponse(BaseModel):
    """充值响应"""
    order_no: str
    amount: Decimal
    tokens: Decimal
    payment_params: Optional[dict] = None

