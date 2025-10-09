from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from decimal import Decimal
from app.core.database import get_db
from app.models.user import User
from app.models.billing import BillingTransaction, RechargeOrder
from app.schemas.billing import TransactionResponse, RechargeRequest, RechargeResponse
from app.schemas.common import ResponseModel
from app.api.dependencies import get_current_user
from app.services.billing import billing_service
import uuid
from datetime import datetime

router = APIRouter()


@router.get("/balance", response_model=ResponseModel)
async def get_balance(
    current_user: User = Depends(get_current_user)
):
    """查询余额"""
    return ResponseModel(
        data={
            "balance": current_user.token_balance,
            "user_id": current_user.id
        }
    )


@router.get("/transactions", response_model=ResponseModel)
async def get_transactions(
    limit: int = 20,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取交易记录"""
    result = await db.execute(
        select(BillingTransaction)
        .where(BillingTransaction.user_id == current_user.id)
        .order_by(BillingTransaction.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    transactions = result.scalars().all()
    
    return ResponseModel(
        data=[TransactionResponse.model_validate(t) for t in transactions]
    )


@router.post("/recharge", response_model=ResponseModel)
async def create_recharge(
    recharge_data: RechargeRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """发起充值"""
    # 生成订单号
    order_no = f"R{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:8].upper()}"
    
    # 计算token数量
    from app.core.config import settings
    tokens = recharge_data.amount / Decimal(settings.TOKEN_PRICE_PER_UNIT)
    
    # 创建充值订单
    order = RechargeOrder(
        user_id=current_user.id,
        order_no=order_no,
        amount=recharge_data.amount,
        tokens=tokens,
        status="pending",
        payment_method=recharge_data.payment_method
    )
    db.add(order)
    await db.commit()
    await db.refresh(order)
    
    # TODO: 调用微信支付接口获取支付参数
    payment_params = {
        "message": "微信支付集成待实现",
        "order_no": order_no
    }
    
    return ResponseModel(
        data=RechargeResponse(
            order_no=order_no,
            amount=recharge_data.amount,
            tokens=tokens,
            payment_params=payment_params
        )
    )


@router.post("/recharge/callback", response_model=ResponseModel)
async def recharge_callback(
    # TODO: 添加微信支付回调参数
    db: AsyncSession = Depends(get_db)
):
    """充值回调（微信支付）"""
    # TODO: 验证微信支付签名
    # TODO: 更新订单状态
    # TODO: 增加用户余额
    
    return ResponseModel(message="回调处理成功")

