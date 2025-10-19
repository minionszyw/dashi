"""
用户相关API
"""
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
import os
import uuid
from pathlib import Path

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate, UserSettings
from app.core.config import settings

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


@router.post("/upload-avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    上传头像
    """
    # 验证文件类型
    allowed_types = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="只支持 JPG、PNG、WEBP 格式的图片")
    
    # 验证文件大小（最大5MB）
    file_content = await file.read()
    if len(file_content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="文件大小不能超过5MB")
    
    # 创建上传目录
    static_dir = Path(__file__).parent.parent.parent.parent / "static" / "avatars"
    static_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成唯一文件名
    file_ext = os.path.splitext(file.filename)[1] or ".jpg"
    filename = f"{uuid.uuid4()}{file_ext}"
    file_path = static_dir / filename
    
    # 保存文件
    with open(file_path, "wb") as f:
        f.write(file_content)
    
    # 生成访问URL
    avatar_url = f"{settings.API_BASE_URL}/static/avatars/{filename}"
    
    # 更新用户头像
    current_user.avatar_url = avatar_url
    db.commit()
    db.refresh(current_user)
    
    return {
        "avatar_url": avatar_url,
        "message": "头像上传成功"
    }

