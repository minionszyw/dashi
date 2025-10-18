"""
订单模型
"""
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class Order(Base):
    """订单表"""
    __tablename__ = "orders"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    amount = Column(Numeric(10, 2), nullable=False, comment="支付金额")
    token_amount = Column(Integer, nullable=False, comment="Token数量")
    status = Column(
        String(20),
        default="pending",
        nullable=False,
        comment="pending/paid/failed/refunded"
    )
    payment_id = Column(String(100), comment="支付平台订单ID")
    trade_no = Column(String(100), unique=True, comment="交易号")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    paid_at = Column(DateTime(timezone=True), comment="支付时间")
    
    def __repr__(self):
        return f"<Order {self.trade_no} ({self.status})>"

