"""
日志 / 审计服务入口。

主要上游：
- admin.html：直接查询日志列表
- rbac_auth_service：关键操作可上报审计日志
- integration_gateway_service：创建订单成功/失败时可上报审计日志

运行示例：
    uvicorn log_audit_service.app.main:app --reload --port 8002
"""

from fastapi import FastAPI

from .database import Base, engine
from .routers import audit_logs


def create_app() -> FastAPI:
    """创建 FastAPI 应用实例并初始化数据库。"""
    # 启动时确保 audit_logs 表存在，避免第一次请求才暴露建表问题。
    Base.metadata.create_all(bind=engine)

    app = FastAPI(title="Log & Audit Service", version="0.1.0")
    # 当前服务所有对外接口都集中在 audit_logs 路由中。
    app.include_router(audit_logs.router)
    return app


app = create_app()
