"""FastAPI 应用入口"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import queues, health
from app.core.config import settings

app = FastAPI(
    title="RabbitMQ Learning API",
    description="Python 学习平台 - RabbitMQ 消息队列实战项目",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(queues.router, prefix="/api")
app.include_router(health.router, prefix="/api")


@app.get("/")
def root():
    return {
        "message": "RabbitMQ Learning API",
        "mode": settings.app_mode,
        "docs": "/docs"
    }
