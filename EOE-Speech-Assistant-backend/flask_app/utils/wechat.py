import httpx
from flask import current_app

async def code2session(code):
    """微信小程序登录：code 换取 openid/session_key"""
    appid = current_app.config['WECHAT_APPID']
    secret = current_app.config['WECHAT_SECRET']
    
    if not appid or not secret:
        # 开发模式：模拟返回
        return {'openid': f'mock_openid_{code}', 'session_key': 'mock_session_key'}
    
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    params = {
        'appid': appid,
        'secret': secret,
        'js_code': code,
        'grant_type': 'authorization_code'
    }
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        return resp.json()
