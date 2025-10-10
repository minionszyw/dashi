from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import datetime
from app.core.database import get_db
from app.core.security import create_access_token
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserLogin, UserResponse
from app.schemas.common import ResponseModel
from app.services.wechat import wechat_service
from app.api.dependencies import get_current_user

router = APIRouter()


@router.post("/wechat/login", response_model=ResponseModel)
async def wechat_login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """微信登录"""
    # 获取微信用户信息
    wechat_data = await wechat_service.code2session(login_data.code)
    if not wechat_data:
        raise HTTPException(status_code=400, detail="微信登录失败")
    
    openid = wechat_data["openid"]
    unionid = wechat_data.get("unionid")
    
    # 查找或创建用户
    result = await db.execute(select(User).where(User.openid == openid))
    user = result.scalar_one_or_none()
    
    if not user:
        # 创建新用户
        user = User(
            openid=openid,
            unionid=unionid,
            token_balance=settings.INITIAL_TOKEN_BALANCE,  # 从环境变量获取初始token
            last_login_at=datetime.utcnow()
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    else:
        # 更新最后登录时间
        await db.execute(
            update(User)
            .where(User.id == user.id)
            .values(last_login_at=datetime.utcnow())
        )
        await db.commit()
    
    # 生成JWT token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return ResponseModel(
        data={
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserResponse.model_validate(user)
        }
    )


@router.get("/user/info", response_model=ResponseModel)
async def get_user_info(
    current_user: User = Depends(get_current_user)
):
    """获取用户信息"""
    return ResponseModel(
        data=UserResponse.model_validate(current_user)
    )


@router.put("/user/info", response_model=ResponseModel)
async def update_user_info(
    user_data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新用户信息"""
    # 更新用户信息
    if "nickname" in user_data:
        current_user.nickname = user_data["nickname"]
    if "avatar_url" in user_data:
        current_user.avatar_url = user_data["avatar_url"]
    
    await db.commit()
    await db.refresh(current_user)
    
    return ResponseModel(
        data=UserResponse.model_validate(current_user),
        message="用户信息更新成功"
    )

