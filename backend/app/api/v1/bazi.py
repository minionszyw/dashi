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
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"收到八字计算请求: user={current_user.id}, data={request.model_dump()}")
        
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
        
        logger.info(f"八字计算成功: {request.name}")
        
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
        
        logger.info(f"八字档案保存成功: profile_id={profile.id}")
        return profile
        
    except Exception as e:
        logger.error(f"八字计算失败: {type(e).__name__}: {str(e)}", exc_info=True)
        db.rollback()
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
    import logging
    from app.models.conversation import Conversation
    
    logger = logging.getLogger(__name__)
    
    profile = db.query(BaziProfile).filter(
        BaziProfile.id == profile_id,
        BaziProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="档案不存在"
        )
    
    try:
        # 先解除所有引用该档案的会话关联
        affected_conversations = db.query(Conversation).filter(
            Conversation.bazi_profile_id == profile_id
        ).update({"bazi_profile_id": None})
        
        if affected_conversations > 0:
            logger.info(f"已解除 {affected_conversations} 个会话的八字档案关联")
        
        # 再删除档案
        db.delete(profile)
        db.commit()
        
        logger.info(f"八字档案删除成功: profile_id={profile_id}")
        return {"message": "删除成功"}
        
    except Exception as e:
        logger.error(f"删除八字档案失败: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除失败：{str(e)}"
        )

