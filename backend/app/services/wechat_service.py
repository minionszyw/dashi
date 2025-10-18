"""
微信API服务
"""
import httpx
from app.core.config import settings


class WeChatService:
    """微信服务"""
    
    def __init__(self):
        self.appid = settings.WX_APPID
        self.secret = settings.WX_SECRET
    
    async def code2session(self, code: str) -> str:
        """
        通过code换取openid
        
        Args:
            code: 微信登录code
            
        Returns:
            openid
        """
        url = "https://api.weixin.qq.com/sns/jscode2session"
        params = {
            "appid": self.appid,
            "secret": self.secret,
            "js_code": code,
            "grant_type": "authorization_code"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            data = response.json()
            
            if "errcode" in data and data["errcode"] != 0:
                raise Exception(f"微信登录失败：{data.get('errmsg', '未知错误')}")
            
            return data["openid"]

