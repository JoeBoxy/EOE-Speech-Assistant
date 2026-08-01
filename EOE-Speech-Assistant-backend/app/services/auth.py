"""
JWT Token 认证服务
"""
from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import HTTPException, status

from app.config import settings
from app.models.user import User


class AuthError(Exception):
    """认证错误"""
    pass


class AuthService:
    """认证服务"""
    
    @classmethod
    def create_token(cls, user: User) -> str:
        """
        为用户创建 JWT Token
        
        Args:
            user: 用户模型实例
            
        Returns:
            JWT Token 字符串
        """
        expire = datetime.utcnow() + timedelta(days=settings.JWT_EXPIRE_DAYS)
        
        payload = {
            "sub": str(user.id),        # 用户 ID
            "openid": user.openid,       # 微信 openid
            "exp": expire,               # 过期时间
            "iat": datetime.utcnow(),    # 签发时间
            "type": "access"             # Token 类型
        }
        
        token = jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
        
        return token
    
    @classmethod
    def verify_token(cls, token: str) -> dict:
        """
        验证 JWT Token
        
        Args:
            token: JWT Token 字符串
            
        Returns:
            Token payload 字典
            
        Raises:
            AuthError: Token 无效或过期
        """
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            
            # 检查 token 类型
            if payload.get("type") != "access":
                raise AuthError("Invalid token type")
            
            return payload
            
        except jwt.ExpiredSignatureError:
            raise AuthError("Token has expired")
        except jwt.InvalidTokenError as e:
            raise AuthError(f"Invalid token: {str(e)}")
    
    @classmethod
    def get_user_id_from_token(cls, token: str) -> int:
        """
        从 token 中获取用户 ID
        
        Args:
            token: JWT Token
            
        Returns:
            用户 ID
        """
        payload = cls.verify_token(token)
        return int(payload["sub"])


# FastAPI OAuth2 风格的错误响应
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid authentication credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
