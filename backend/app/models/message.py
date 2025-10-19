"""
消息模型
"""
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class Message(Base):
    """消息表"""
    __tablename__ = "messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(
        UUID(as_uuid=True),
        ForeignKey("conversations.id"),
        nullable=False,
        index=True
    )
    role = Column(String(20), nullable=False, comment="user/assistant/system")
    content = Column(Text, nullable=False, comment="消息内容")
    token_cost = Column(Integer, default=0, comment="Token消耗")
    extra_data = Column(JSONB, comment="元数据")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # 关系
    conversation = relationship("Conversation", back_populates="messages")
    
    def __repr__(self):
        return f"<Message {self.role} ({self.id})>"

