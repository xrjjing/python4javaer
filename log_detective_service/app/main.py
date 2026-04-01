"""
日志侦探服务入口。

真实调用链通常是：
log-detective.html
    -> integration_gateway_service /gateway/log-detective/analyze
    -> 本服务 /internal/log-detective/analyze
    -> analyzer.py

排查建议：
- 网关能通但分析接口 404/500 时，先看这里是否正确挂载 router 和前缀。
"""

from fastapi import FastAPI
from .config import settings
from .routers import log_detective

# 应用入口：当前服务的业务路由集中在 log_detective.router 中。
app = FastAPI(title=settings.SERVICE_NAME)

# 业务路由统一挂到 /internal/log-detective 下，
# 这样网关层可以稳定地把外部请求转发到一个固定前缀。
app.include_router(log_detective.router, prefix="/internal/log-detective")

@app.get("/health")
def health():
    """服务级健康检查。"""
    return {"status": "ok"}
