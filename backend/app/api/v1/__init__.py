from fastapi import APIRouter
from app.api.v1 import auth, chat, billing

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(chat.router, prefix="/chat", tags=["对话"])
api_router.include_router(billing.router, prefix="/billing", tags=["计费"])

