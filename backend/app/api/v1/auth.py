"""
认证相关API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token
from app.core.config import settings
from app.models.user import User
from app.schemas.auth import WxLoginRequest, WxLoginResponse
from app.services.wechat_service import WeChatService

router = APIRouter()
wechat_service = WeChatService()


@router.post("/wx-login", response_model=WxLoginResponse)
async def wx_login(
    request: WxLoginRequest,
    db: Session = Depends(get_db)
):
    """
    微信登录
    
    使用微信code换取openid，创建或获取用户信息
    """
    try:
        # 获取微信openid
        openid = await wechat_service.code2session(request.code)
        
        # 查找或创建用户
        user = db.query(User).filter(User.openid == openid).first()
        is_new_user = False
        
        if not user:
            # 创建新用户
            user = User(
                openid=openid,
                token_balance=settings.INITIAL_TOKEN_BALANCE
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            is_new_user = True
        
        # 生成JWT token
        access_token = create_access_token(data={"sub": str(user.id)})
        
        return WxLoginResponse(
            token=access_token,
            user={
                "id": str(user.id),
                "nickname": user.nickname,
                "avatar_url": user.avatar_url,
                "token_balance": user.token_balance
            },
            is_new_user=is_new_user
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"登录失败：{str(e)}"
        )

