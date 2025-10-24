"""API v1"""
from fastapi import APIRouter

from app.api.v1 import auth, user, bazi, chat, share

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(user.router, prefix="/user", tags=["用户"])
api_router.include_router(bazi.router, prefix="/bazi", tags=["八字"])
api_router.include_router(chat.router, prefix="/chat", tags=["对话"])
api_router.include_router(share.router, prefix="/share", tags=["分享"])

