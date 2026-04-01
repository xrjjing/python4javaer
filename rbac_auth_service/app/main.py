"""
RBAC 服务入口。

上游：
- login.html：登录与获取当前用户
- admin.html：用户 / 角色 / 权限管理

下游：
- routers/*：按功能拆分的 API 层
- database.py：建表与会话

排查建议：
- 路由没挂上、统一异常格式不对、静态后台页访问异常时，先看这里。
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from starlette.requests import Request

from .database import Base, engine
from .routers import auth, roles, users, todos, projects, tasks
from .schemas import APIResponse, ErrorCode


def create_app() -> FastAPI:
    """应用工厂函数，创建并配置 FastAPI 实例。"""
    app = FastAPI(title="RBAC 示例 API")

    # 启动阶段的基础设施初始化：本地学习模式下直接在这里建表，避免首次启动前还要手工迁移。
    Base.metadata.create_all(bind=engine)

    # HTTP 入口注册区：login.html / admin.html 最终都会命中这里挂上的各类 router。
    app.include_router(auth.router)
    app.include_router(users.router)
    app.include_router(roles.router)
    app.include_router(todos.router)
    app.include_router(projects.router)
    app.include_router(tasks.router)

    # 统一异常包装：把不同 router 抛出的 HTTPException 转成统一 APIResponse 结构。
    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request, exc: HTTPException
    ):  # type: ignore[override]
        # 若 detail 中包含 code/message，则优先使用
        code = ErrorCode.INTERNAL_ERROR
        message = "请求错误"
        data = None

        if isinstance(exc.detail, dict) and "code" in exc.detail:
            try:
                code = ErrorCode(exc.detail["code"])
            except ValueError:
                code = ErrorCode.INTERNAL_ERROR
            message = exc.detail.get("message", message)
            data = exc.detail.get("data")
        else:
            mapping = {
                status.HTTP_401_UNAUTHORIZED: ErrorCode.UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN: ErrorCode.FORBIDDEN,
                status.HTTP_404_NOT_FOUND: ErrorCode.NOT_FOUND,
                status.HTTP_400_BAD_REQUEST: ErrorCode.BAD_REQUEST,
            }
            code = mapping.get(exc.status_code, ErrorCode.INTERNAL_ERROR)
            if isinstance(exc.detail, str):
                message = exc.detail

        resp = APIResponse(code=code, message=message, data=data)
        return JSONResponse(status_code=exc.status_code, content=resp.model_dump())

    # 请求体验证错误统一包装：前端看到的字段校验错误最终会经过这里。
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):  # type: ignore[override]
        resp = APIResponse(
            code=ErrorCode.VALIDATION_ERROR,
            message="请求参数验证失败",
            data=exc.errors(),
        )
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=resp.model_dump())

    # 兜底异常处理
    @app.exception_handler(Exception)
    async def generic_exception_handler(
        request: Request, exc: Exception
    ):  # type: ignore[override]
        # 这里可以根据需要记录日志，目前只返回通用错误响应
        resp = APIResponse(
            code=ErrorCode.INTERNAL_ERROR,
            message="服务器内部错误",
            data=None,
        )
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=resp.model_dump())

    # 静态前端：旧版 RBAC 管理控制台挂载点。
    # 当前主用的是 frontend/login.html 和 frontend/admin.html，旧页面仍保留作兼容演示。
    static_dir = Path(__file__).resolve().parent / "static"
    if static_dir.exists():
        app.mount(
            "/rbac-admin",
            StaticFiles(directory=static_dir, html=True),
            name="rbac-admin",
        )

    return app


app = create_app()
