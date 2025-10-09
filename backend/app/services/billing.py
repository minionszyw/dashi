from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models.user import User
from app.models.billing import BillingTransaction
from app.core.config import settings
from datetime import datetime


class BillingService:
    """计费服务"""
    
    @staticmethod
    async def check_balance(db: AsyncSession, user_id: int, required_tokens: Decimal) -> bool:
        """检查余额是否充足"""
        result = await db.execute(
            select(User.token_balance).where(User.id == user_id)
        )
        balance = result.scalar_one()
        return balance >= required_tokens
    
    @staticmethod
    async def deduct_tokens(
        db: AsyncSession,
        user_id: int,
        tokens: int,
        description: str,
        reference_id: str = None
    ) -> bool:
        """扣除token"""
        # 获取当前余额
        result = await db.execute(
            select(User.token_balance).where(User.id == user_id)
        )
        current_balance = result.scalar_one()
        
        # 计算扣费金额
        cost = Decimal(tokens) * Decimal(settings.AI_COST_PER_TOKEN)
        
        if current_balance < cost:
            return False
        
        # 扣除余额
        new_balance = current_balance - cost
        await db.execute(
            update(User)
            .where(User.id == user_id)
            .values(token_balance=new_balance)
        )
        
        # 记录交易
        transaction = BillingTransaction(
            user_id=user_id,
            type="consume",
            amount=-cost,
            balance_after=new_balance,
            description=description,
            reference_id=reference_id
        )
        db.add(transaction)
        
        await db.commit()
        return True
    
    @staticmethod
    async def add_tokens(
        db: AsyncSession,
        user_id: int,
        amount: Decimal,
        description: str,
        reference_id: str = None
    ) -> Decimal:
        """充值token"""
        # 计算token数量（按价格比例）
        tokens = amount / Decimal(settings.TOKEN_PRICE_PER_UNIT)
        
        # 获取当前余额
        result = await db.execute(
            select(User.token_balance).where(User.id == user_id)
        )
        current_balance = result.scalar_one()
        
        # 增加余额
        new_balance = current_balance + tokens
        await db.execute(
            update(User)
            .where(User.id == user_id)
            .values(token_balance=new_balance)
        )
        
        # 记录交易
        transaction = BillingTransaction(
            user_id=user_id,
            type="recharge",
            amount=amount,
            balance_after=new_balance,
            description=description,
            reference_id=reference_id
        )
        db.add(transaction)
        
        await db.commit()
        return new_balance


billing_service = BillingService()

