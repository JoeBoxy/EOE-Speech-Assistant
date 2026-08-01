"""
用户相关数据模型
"""
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.base import Response


class UserUpdateRequest(BaseModel):
    """更新用户信息请求"""
    nickname: Optional[str] = Field(None, description="用户昵称")
    avatar_url: Optional[str] = Field(None, description="用户头像 URL")


class UserInfoData(BaseModel):
    """用户信息数据"""
    id: int
    nickname: Optional[str]
    avatar_url: Optional[str]
    created_at: Optional[str]


class UserInfoResponse(Response[UserInfoData]):
    """用户信息响应"""
    pass
