from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # App
    APP_NAME: str = "国学大师"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str
    
    # Redis
    REDIS_URL: str
    
    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days
    
    # WeChat
    WECHAT_APPID: str
    WECHAT_SECRET: str
    
    # DeepSeek AI
    DEEPSEEK_API_KEY: str
    DEEPSEEK_API_BASE: str = "https://api.deepseek.com/v1"
    DEEPSEEK_MODEL: str = "deepseek-chat"
    
    # Token Pricing
    TOKEN_PRICE_PER_UNIT: float = 0.01
    AI_COST_PER_TOKEN: float = 0.001
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 10
    RATE_LIMIT_PER_DAY: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

