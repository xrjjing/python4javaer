"""
系统对接网关服务入口。

运行示例：
    uvicorn integration_gateway_service.app.main:app --reload
"""

from fastapi import FastAPI

from .routers import gateway


def create_app() -> FastAPI:
    """创建 FastAPI 应用实例，并挂载网关路由。"""
    app = FastAPI(title="Integration Gateway Service", version="0.1.0")
    app.include_router(gateway.router)
    return app


app = create_app()

