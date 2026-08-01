"""
SQLAlchemy 基础配置
支持 SQLite 和 MySQL 双数据库
"""
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, func
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column, sessionmaker

from app.config import settings


class Base(AsyncAttrs, DeclarativeBase):
    """数据库模型基类"""
    
    # 自动将类名转为小写表名
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    
    # 通用字段
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="创建时间"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新时间"
    )


# 获取数据库 URL (兼容 SQLite 和 MySQL)
database_url = settings.database_url

# 如果是 SQLite，确保使用异步驱动
if database_url.startswith("sqlite:///"):
    # 转换为异步 SQLite URL
    async_database_url = database_url.replace("sqlite:///", "sqlite+aiosqlite:///")
else:
    async_database_url = database_url

# 创建异步引擎
engine = create_async_engine(
    async_database_url,
    echo=settings.debug,  # DEBUG 模式打印 SQL
    future=True
)

# 创建异步会话工厂
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


async def get_db() -> AsyncSession:
    """获取数据库会话 (用于 FastAPI Dependency)"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """初始化数据库表"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
