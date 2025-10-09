from sqlalchemy import Column, BigInteger, String, DECIMAL, TIMESTAMP, func
from app.core.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(BigInteger, primary_key=True, index=True)
    openid = Column(String(128), unique=True, nullable=False, index=True)
    unionid = Column(String(128), nullable=True)
    nickname = Column(String(64), nullable=True)
    avatar_url = Column(String(512), nullable=True)
    token_balance = Column(DECIMAL(10, 2), default=0, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
    last_login_at = Column(TIMESTAMP, nullable=True)

