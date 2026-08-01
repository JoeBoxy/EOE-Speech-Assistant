"""
登录认证路由
POST /api/auth/login - 微信小程序登录
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, LoginResponse
from app.services.auth import AuthService
from app.services.wechat import WechatError, WechatService

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    """
    微信小程序登录
    
    1. 接收小程序传来的 code
    2. 用 code 向微信服务器换取 openid
    3. 查询或创建用户
    4. 生成 JWT token 返回
    """
    try:
        # 1. 用 code 换取 openid 和 session_key
        wechat_data = await WechatService.code2session(request.code)
        openid = wechat_data["openid"]
        session_key = wechat_data.get("session_key")
        unionid = wechat_data.get("unionid")
        
        # 2. 查询用户是否已存在
        result = await db.execute(select(User).where(User.openid == openid))
        user = result.scalar_one_or_none()
        
        if user:
            # 更新 session_key
            user.session_key = session_key
            if unionid and not user.unionid:
                user.unionid = unionid
        else:
            # 创建新用户
            user = User(
                openid=openid,
                unionid=unionid,
                session_key=session_key,
                nickname=request.nickname,
                avatar_url=request.avatar_url
            )
            db.add(user)
        
        await db.commit()
        await db.refresh(user)
        
        # 3. 生成 JWT token
        token = AuthService.create_token(user)
        
        return {
            "code": 0,
            "message": "success",
            "data": {
                "token": token,
                "expire_days": 7,
                "user_info": user.to_dict()
            }
        }
        
    except WechatError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": 1001,
                "message": f"Wechat login failed: {e.message}"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": 500,
                "message": f"Internal server error: {str(e)}"
            }
        )
