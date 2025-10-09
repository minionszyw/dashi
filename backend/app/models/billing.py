from sqlalchemy import Column, BigInteger, String, Text, DECIMAL, TIMESTAMP, ForeignKey, func
from app.core.database import Base


class BillingTransaction(Base):
    __tablename__ = "billing_transactions"
    
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True)
    type = Column(String(20), nullable=False)  # recharge, consume, refund
    amount = Column(DECIMAL(10, 2), nullable=False)
    balance_after = Column(DECIMAL(10, 2), nullable=True)
    description = Column(Text, nullable=True)
    reference_id = Column(String(128), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)


class RechargeOrder(Base):
    __tablename__ = "recharge_orders"
    
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True)
    order_no = Column(String(64), unique=True, nullable=False, index=True)
    amount = Column(DECIMAL(10, 2), nullable=False)
    tokens = Column(DECIMAL(10, 2), nullable=False)
    status = Column(String(20), default="pending", nullable=False)  # pending, paid, failed, refunded
    payment_method = Column(String(20), nullable=True)  # wechat
    transaction_id = Column(String(128), nullable=True)
    paid_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

