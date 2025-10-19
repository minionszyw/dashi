"""
应用配置管理
"""
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """应用配置"""
    
    # 应用信息
    APP_NAME: str = "大师AI命理"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # 数据库配置
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    REDIS_URL: str = Field(..., env="REDIS_URL")
    
    # 微信配置
    WX_APPID: str = Field(..., env="WX_APPID")
    WX_SECRET: str = Field(..., env="WX_SECRET")
    WX_MCH_ID: str = Field(default="", env="WX_MCH_ID")
    WX_API_KEY: str = Field(default="", env="WX_API_KEY")
    
    # OpenAI配置
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    OPENAI_MODEL: str = Field(default="gpt-4", env="OPENAI_MODEL")
    OPENAI_BASE_URL: str = Field(
        default="https://api.openai.com/v1",
        env="OPENAI_BASE_URL"
    )
    OPENAI_TEMPERATURE: float = Field(default=0.7, env="OPENAI_TEMPERATURE")
    OPENAI_MAX_TOKENS: int = Field(default=2000, env="OPENAI_MAX_TOKENS")
    
    # 业务配置
    INITIAL_TOKEN_BALANCE: int = Field(default=10000, env="INITIAL_TOKEN_BALANCE")  # 单位：分
    TOKEN_PRICE_RATE: float = Field(default=0.01, env="TOKEN_PRICE_RATE")
    
    # 安全配置
    JWT_SECRET_KEY: str = Field(..., env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = Field(default="HS256", env="JWT_ALGORITHM")
    JWT_EXPIRE_MINUTES: int = Field(default=10080, env="JWT_EXPIRE_MINUTES")
    
    # CORS配置
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000"],
        env="CORS_ORIGINS"
    )
    
    # 日志配置
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# 创建全局配置实例
settings = Settings()

