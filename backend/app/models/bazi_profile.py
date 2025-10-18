"""
八字档案模型
"""
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class BaziProfile(Base):
    """八字档案表"""
    __tablename__ = "bazi_profiles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(50), comment="姓名")
    gender = Column(String(10), comment="性别")
    birth_info = Column(JSONB, nullable=False, comment="出生信息")
    bazi_result = Column(JSONB, comment="八字排盘结果")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<BaziProfile {self.name} ({self.id})>"

