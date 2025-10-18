"""
用户模型
"""
from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class User(Base):
    """用户表"""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    openid = Column(String(100), unique=True, nullable=False, index=True)
    nickname = Column(String(50))
    avatar_url = Column(Text)
    gender = Column(String(10))
    birth_info = Column(JSONB, comment="出生信息")
    token_balance = Column(Integer, default=100, nullable=False, comment="Token余额")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<User {self.nickname} ({self.id})>"

