"""
EOE演讲线上助手 Backend - FastAPI 应用入口
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.models.base import init_db
from app.routers import auth, user


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化数据库
    await init_db()
    print(f"🚀 {settings.app_name} started!")
    print(f"🔧 Environment: {settings.current_env}")
    print(f"📁 Database: {settings.database_url}")
    print(f"🐛 Debug: {settings.debug}")
    yield
    # 关闭时清理资源
    print("👋 Server shutting down...")


# 创建 FastAPI 应用
app = FastAPI(
    title=settings.app_name,
    description="EOE演讲线上助手微信小程序后端 API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,  # 生产环境关闭文档
    redoc_url="/redoc" if settings.debug else None
)

# CORS 配置 - 允许微信小程序域名
# 生产环境应限制为小程序域名
default_origins = ["*"] if settings.debug else []
cors_origins = settings.get("cors_origins", default_origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 健康检查
@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.current_env
    }


# 注册路由
app.include_router(auth.router, prefix="/api")
app.include_router(user.router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
