"""
RBAC 示例 FastAPI 应用入口。

运行方式：

    cd rbac_auth_service
    uvicorn app.main:app --reload
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.requests import Request

from .database import Base, engine
from .routers import auth, roles, users, todos, projects, tasks
from .schemas import APIResponse, ErrorCode


def create_app() -> FastAPI:
    """应用工厂函数，创建并配置 FastAPI 实例。"""
    app = FastAPI(title="RBAC 示例 API")

    # 确保数据库表已创建
    Base.metadata.create_all(bind=engine)

    # 挂载路由
    app.include_router(auth.router)
    app.include_router(users.router)
    app.include_router(roles.router)
    app.include_router(todos.router)
    app.include_router(projects.router)
    app.include_router(tasks.router)

    # 统一异常处理：HTTPException
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

    # 请求体验证错误
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

    return app


app = create_app()
