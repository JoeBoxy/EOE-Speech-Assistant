"""
微信 API 服务封装
处理微信登录、获取 openid 等操作
"""
import httpx

from app.config import settings


class WechatError(Exception):
    """微信 API 错误"""
    def __init__(self, message: str, errcode: int = None):
        self.message = message
        self.errcode = errcode
        super().__init__(self.message)


class WechatService:
    """微信服务"""
    
    BASE_URL = "https://api.weixin.qq.com"
    
    @classmethod
    async def code2session(cls, code: str) -> dict:
        """
        小程序登录 - 用 code 换取 openid 和 session_key
        
        Args:
            code: wx.login() 获取的临时登录凭证
            
        Returns:
            {
                "openid": "用户唯一标识",
                "session_key": "会话密钥",
                "unionid": "用户在开放平台的唯一标识符" (可能为空)
            }
            
        Raises:
            WechatError: 微信 API 返回错误
        """
        url = f"{cls.BASE_URL}/sns/jscode2session"
        params = {
            "appid": settings.WECHAT_APPID,
            "secret": settings.WECHAT_SECRET,
            "js_code": code,
            "grant_type": "authorization_code"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
        
        # 检查错误
        if "errcode" in data and data["errcode"] != 0:
            raise WechatError(
                message=data.get("errmsg", "Unknown error"),
                errcode=data["errcode"]
            )
        
        # 检查必要字段
        if "openid" not in data:
            raise WechatError("微信返回数据缺少 openid")
        
        return {
            "openid": data["openid"],
            "session_key": data.get("session_key"),
            "unionid": data.get("unionid")
        }
