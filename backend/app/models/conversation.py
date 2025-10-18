"""
会话模型
"""
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class Conversation(Base):
    """会话表"""
    __tablename__ = "conversations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(100), default="新会话")
    bazi_profile_id = Column(UUID(as_uuid=True), ForeignKey("bazi_profiles.id"), nullable=True)
    context_size = Column(Integer, default=10, comment="上下文消息数")
    ai_style = Column(String(50), default="professional", comment="AI风格")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True, index=True, comment="软删除时间")
    
    # 关系
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Conversation {self.title} ({self.id})>"

