"""
认证相关数据模型
"""
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.base import Response


class LoginRequest(BaseModel):
    """登录请求"""
    code: str = Field(..., description="微信小程序 login 返回的 code")
    nickname: Optional[str] = Field(None, description="用户昵称")
    avatar_url: Optional[str] = Field(None, description="用户头像 URL")


class UserInfo(BaseModel):
    """用户信息"""
    id: int
    nickname: Optional[str]
    avatar_url: Optional[str]
    created_at: Optional[str]


class LoginData(BaseModel):
    """登录成功返回的数据"""
    token: str = Field(..., description="JWT Token")
    expire_days: int = Field(7, description="Token 有效期（天）")
    user_info: UserInfo


class LoginResponse(Response[LoginData]):
    """登录响应"""
    pass
