# app/main.py
"""
FastAPI 应用入口
演示多级依赖链：Settings → Engine → Session → Repository → Route
"""
from fastapi import FastAPI

from .models import Base
from .db import get_engine
from .config import get_settings
from .routers import users


def create_app(init_db: bool = True) -> FastAPI:
    """
    应用工厂，便于测试时创建独立实例

    Args:
        init_db: 是否初始化数据库，测试时设为 False
    """
    app = FastAPI(
        title="Lab02: Dependency Chain Override",
        description="演示多级依赖链与测试覆盖",
        version="1.0.0",
    )

    # 挂载路由
    app.include_router(users.router)

    # 健康检查
    @app.get("/health", tags=["health"])
    def health():
        return {"status": "ok"}

    # 启动时初始化数据库（可通过参数禁用）
    if init_db:
        @app.on_event("startup")
        def on_startup():
            _init_db()

    return app


def _init_db():
    """初始化数据库表（生产环境启动时调用）"""
    settings = get_settings()
    engine = get_engine(settings)
    Base.metadata.create_all(engine)


# 创建应用实例（生产环境）
app = create_app(init_db=True)


# 运行：uvicorn app.main:app --reload
