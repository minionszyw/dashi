"""
分享功能API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import httpx
import base64

from app.core.database import get_db
from app.models.user import User
from app.models.conversation import Conversation
from app.api.v1.auth import get_current_user
from app.core.config import settings

router = APIRouter()


class MiniProgramCodeRequest(BaseModel):
    """小程序码生成请求"""
    conversation_id: str
    page: str = "pages/session/index"  # 使用TabBar页面，扫码后从会话列表进入


@router.post("/miniprogram-code")
async def generate_miniprogram_code(
    request: MiniProgramCodeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    生成小程序码
    
    用于分享会话海报，扫码后可直接打开对应会话
    """
    # 验证会话是否属于当前用户
    conversation = db.query(Conversation).filter(
        Conversation.id == request.conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="会话不存在"
        )
    
    # 构造场景参数（微信限制32字符）
    # 去掉UUID中的横线，取后24位（加上cid=共28字符）
    conv_id_short = str(request.conversation_id).replace('-', '')[-24:]
    scene = f"cid={conv_id_short}"
    
    # 调用微信接口生成小程序码
    # 注意：这需要微信小程序的access_token
    # 实际生产环境需要实现access_token的获取和缓存机制
    
    # 检查微信配置
    if not settings.WX_APPID or not settings.WX_SECRET or settings.WX_APPID == "wxxxxxxxxxxx":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="分享功能未配置，请联系管理员配置微信小程序凭证"
        )
    
    try:
        # 获取access_token（简化示例，实际应该缓存）
        token_url = "https://api.weixin.qq.com/cgi-bin/token"
        token_params = {
            "grant_type": "client_credential",
            "appid": settings.WX_APPID,
            "secret": settings.WX_SECRET
        }
        
        async with httpx.AsyncClient() as client:
            token_response = await client.get(token_url, params=token_params, timeout=10.0)
            token_data = token_response.json()
            
            if "access_token" not in token_data:
                error_msg = token_data.get("errmsg", "未知错误")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"获取微信access_token失败: {error_msg}"
                )
            
            access_token = token_data["access_token"]
            
            # 生成小程序码
            code_url = f"https://api.weixin.qq.com/wxa/getwxacodeunlimit?access_token={access_token}"
            code_params = {
                "scene": scene,
                "page": request.page,  # 正式发布版本：直接跳转到指定页面
                "width": 280,
                "auto_color": False,
                "line_color": {"r": 44, "g": 62, "b": 80},  # $primary颜色
                "is_hyaline": True  # 透明底色
            }
            
            code_response = await client.post(code_url, json=code_params, timeout=10.0)
            
            if code_response.headers.get("content-type") == "image/jpeg":
                # 成功获取图片，转为base64返回
                image_base64 = base64.b64encode(code_response.content).decode()
                return {
                    "code": 0,
                    "message": "success",
                    "data": {
                        "image_base64": f"data:image/jpeg;base64,{image_base64}",
                        "conversation_id": request.conversation_id
                    }
                }
            else:
                error_data = code_response.json()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"生成小程序码失败: {error_data.get('errmsg', '未知错误')}"
                )
    
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"调用微信接口失败: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"生成小程序码异常: {str(e)}"
        )

