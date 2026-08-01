"""
用户信息路由
GET    /api/user/info - 获取当前用户信息
PUT    /api/user/info - 更新用户信息
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.middlewares.auth import get_current_user
from app.models.base import get_db
from app.models.user import User
from app.schemas.user import UserInfoResponse, UserUpdateRequest

router = APIRouter(prefix="/user", tags=["用户"])


@router.get("/info", response_model=UserInfoResponse)
async def get_user_info(
    current_user: User = Depends(get_current_user)
):
    """获取当前登录用户信息"""
    return {
        "code": 0,
        "message": "success",
        "data": current_user.to_dict()
    }


@router.put("/info", response_model=UserInfoResponse)
async def update_user_info(
    request: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新当前用户信息 (昵称、头像)"""
    # 只更新提供的字段
    if request.nickname is not None:
        current_user.nickname = request.nickname
    if request.avatar_url is not None:
        current_user.avatar_url = request.avatar_url
    
    await db.commit()
    await db.refresh(current_user)
    
    return {
        "code": 0,
        "message": "success",
        "data": current_user.to_dict()
    }
