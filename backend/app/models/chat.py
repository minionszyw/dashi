from sqlalchemy import Column, BigInteger, String, Text, Integer, TIMESTAMP, ForeignKey, func
from app.core.database import Base


class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(128), nullable=True)
    status = Column(String(20), default="active", nullable=False)  # active, archived, deleted
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(BigInteger, primary_key=True, index=True)
    session_id = Column(BigInteger, ForeignKey("chat_sessions.id"), nullable=False, index=True)
    role = Column(String(20), nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    tokens_used = Column(Integer, default=0, nullable=False)
    model = Column(String(64), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

