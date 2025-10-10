"""
管理员API
"""
from fastapi import APIRouter, Depends, HTTPException
from app.core.prompts import get_system_prompt, list_available_prompts, SYSTEM_PROMPTS
from app.schemas.common import ResponseModel

router = APIRouter()

@router.get("/prompts", response_model=ResponseModel)
async def get_available_prompts():
    """获取可用的系统提示词风格"""
    return ResponseModel(
        data={
            "available_styles": list_available_prompts(),
            "current_style": "default"
        }
    )

@router.get("/prompts/{style}", response_model=ResponseModel)
async def get_prompt_by_style(style: str):
    """获取指定风格的系统提示词"""
    if style not in SYSTEM_PROMPTS:
        raise HTTPException(status_code=404, detail="提示词风格不存在")
    
    return ResponseModel(
        data={
            "style": style,
            "content": get_system_prompt(style)
        }
    )
