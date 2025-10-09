import httpx
from app.core.config import settings
from typing import Optional, Dict


class WeChatService:
    """微信服务"""
    
    @staticmethod
    async def code2session(code: str) -> Optional[Dict]:
        """微信code换取session_key和openid"""
        url = "https://api.weixin.qq.com/sns/jscode2session"
        params = {
            "appid": settings.WECHAT_APPID,
            "secret": settings.WECHAT_SECRET,
            "js_code": code,
            "grant_type": "authorization_code"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            data = response.json()
            
            if "errcode" in data and data["errcode"] != 0:
                return None
            
            return {
                "openid": data.get("openid"),
                "session_key": data.get("session_key"),
                "unionid": data.get("unionid")
            }


wechat_service = WeChatService()

