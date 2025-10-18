"""
用户相关API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate, UserSettings

router = APIRouter()


@router.get("/profile", response_model=UserResponse)
async def get_profile(
    current_user: User = Depends(get_current_user)
):
    """获取用户信息"""
    return current_user


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    update_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新用户信息"""
    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("/settings", response_model=UserSettings)
async def get_settings(
    current_user: User = Depends(get_current_user)
):
    """获取用户设置"""
    # TODO: 从数据库或Redis获取用户设置
    return UserSettings()


@router.put("/settings", response_model=UserSettings)
async def update_settings(
    settings: UserSettings,
    current_user: User = Depends(get_current_user)
):
    """更新用户设置"""
    # TODO: 保存用户设置到数据库或Redis
    return settings

