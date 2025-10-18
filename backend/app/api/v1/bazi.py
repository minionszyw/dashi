"""
八字相关API
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.bazi_profile import BaziProfile
from app.schemas.bazi import BaziCalculateRequest, BaziProfileResponse
from app.services.bazi_service import BaziService

router = APIRouter()
bazi_service = BaziService()


@router.post("/calculate", response_model=BaziProfileResponse)
async def calculate_bazi(
    request: BaziCalculateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    计算八字并保存档案
    """
    try:
        # 计算八字
        bazi_result = bazi_service.calculate(
            name=request.name,
            gender=request.gender,
            calendar=request.calendar,
            year=request.year,
            month=request.month,
            day=request.day,
            hour=request.hour,
            minute=request.minute,
            birth_city=request.birth_city,
            current_city=request.current_city
        )
        
        # 保存档案
        profile = BaziProfile(
            user_id=current_user.id,
            name=request.name,
            gender=request.gender,
            birth_info=request.model_dump(),
            bazi_result=bazi_result
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
        
        return profile
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"八字计算失败：{str(e)}"
        )


@router.get("/profiles", response_model=List[BaziProfileResponse])
async def get_profiles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取用户的八字档案列表"""
    profiles = db.query(BaziProfile).filter(
        BaziProfile.user_id == current_user.id
    ).order_by(BaziProfile.created_at.desc()).all()
    
    return profiles


@router.get("/profiles/{profile_id}", response_model=BaziProfileResponse)
async def get_profile(
    profile_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取八字档案详情"""
    profile = db.query(BaziProfile).filter(
        BaziProfile.id == profile_id,
        BaziProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="档案不存在"
        )
    
    return profile


@router.delete("/profiles/{profile_id}")
async def delete_profile(
    profile_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除八字档案"""
    profile = db.query(BaziProfile).filter(
        BaziProfile.id == profile_id,
        BaziProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="档案不存在"
        )
    
    db.delete(profile)
    db.commit()
    
    return {"message": "删除成功"}

