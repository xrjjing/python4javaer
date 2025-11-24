from fastapi import FastAPI

from .database import Base, engine
from .routers import todos


def create_app() -> FastAPI:
    """应用工厂函数，创建并配置 FastAPI 实例。"""
    app = FastAPI(title="TODO API（SQLite 版）")

    # 确保数据库表已创建
    Base.metadata.create_all(bind=engine)

    # 挂载路由
    app.include_router(todos.router)
    return app


app = create_app()

