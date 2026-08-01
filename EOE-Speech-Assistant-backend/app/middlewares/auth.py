"""
认证中间件
验证 JWT Token，获取当前用户
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import get_db
from app.models.user import User
from app.services.auth import AuthError, AuthService

# 使用 HTTP Bearer Token 认证
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    获取当前登录用户
    
    从请求头中提取 Authorization: Bearer <token>
    验证 token 并返回对应的用户
    """
    token = credentials.credentials
    
    try:
        # 验证 token
        user_id = AuthService.get_user_id_from_token(token)
        
        # 查询用户
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "code": 1002,
                    "message": "User not found"
                },
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user
        
    except AuthError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": 1002,
                "message": str(e)
            },
            headers={"WWW-Authenticate": "Bearer"},
        )
