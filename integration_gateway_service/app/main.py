"""
系统对接网关服务入口。

这个服务位于前端与多个下游服务之间，主要负责：
- 校验来自 RBAC 的 JWT；
- 把请求转发给下游服务；
- 统一把下游异常转换成更适合前端理解的 HTTP 错误；
- 在部分关键操作后补发审计日志。

重点调用链：
- log-detective.html -> /gateway/log-detective/analyze -> log_detective_service
- 客户端 -> /gateway/backend/* -> backend_user_order_service
"""

from fastapi import FastAPI

from .routers import gateway


def create_app() -> FastAPI:
    """创建 FastAPI 应用实例，并挂载网关路由。"""
    app = FastAPI(title="Integration Gateway Service", version="0.1.0")
    # 当前网关的所有对外入口都集中在 routers/gateway.py 中。
    app.include_router(gateway.router)
    return app


app = create_app()
