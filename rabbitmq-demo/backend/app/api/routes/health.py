"""健康检查和模式查询"""
from fastapi import APIRouter
from app.core.config import settings
from app.core.rabbit import get_connection
import pika

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check():
    """健康检查"""
    status = "ok"
    details = {"mode": settings.app_mode}

    if settings.app_mode == "real":
        try:
            conn = get_connection()
            if not conn.is_open:
                status = "degraded"
                details["rabbitmq"] = "connection closed"
            else:
                details["rabbitmq"] = "connected"
        except pika.exceptions.AMQPConnectionError:
            status = "degraded"
            details["rabbitmq"] = "unavailable"

    return {"status": status, **details}


@router.get("/mode")
def get_mode():
    """获取当前运行模式"""
    return {"mode": settings.app_mode}
