"""
日志 / 审计服务入口。

运行示例：
    uvicorn log_audit_service.app.main:app --reload --port 8002
"""

from fastapi import FastAPI

from .database import Base, engine
from .routers import audit_logs


def create_app() -> FastAPI:
    """创建 FastAPI 应用实例并初始化数据库。"""
    Base.metadata.create_all(bind=engine)

    app = FastAPI(title="Log & Audit Service", version="0.1.0")
    app.include_router(audit_logs.router)
    return app


app = create_app()

