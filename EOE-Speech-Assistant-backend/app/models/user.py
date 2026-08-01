"""
用户模型
"""
from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class User(Base):
    """用户表"""
    
    # 微信相关 (核心字段)
    openid: Mapped[str] = mapped_column(
        String(64), 
        unique=True, 
        index=True,
        comment="微信用户唯一标识"
    )
    unionid: Mapped[Optional[str]] = mapped_column(
        String(64), 
        nullable=True,
        comment="微信开放平台统一标识"
    )
    
    # 用户信息
    nickname: Mapped[Optional[str]] = mapped_column(
        String(128), 
        nullable=True,
        comment="用户昵称"
    )
    avatar_url: Mapped[Optional[str]] = mapped_column(
        String(512), 
        nullable=True,
        comment="头像 URL"
    )
    
    # 微信 session_key (用于敏感数据解密)
    session_key: Mapped[Optional[str]] = mapped_column(
        String(64), 
        nullable=True,
        comment="微信 session_key"
    )
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, openid={self.openid}, nickname={self.nickname})>"
    
    def to_dict(self) -> dict:
        """转换为字典 (用于 API 响应)"""
        return {
            "id": self.id,
            "nickname": self.nickname,
            "avatar_url": self.avatar_url,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
