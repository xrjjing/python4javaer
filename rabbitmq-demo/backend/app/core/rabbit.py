"""RabbitMQ 连接管理"""
import pika
import threading
from app.core.config import settings

_connection_lock = threading.Lock()
_connection = None


def get_connection() -> pika.BlockingConnection:
    """获取 RabbitMQ 连接（单例模式）"""
    global _connection
    with _connection_lock:
        if _connection and _connection.is_open:
            return _connection

        credentials = pika.PlainCredentials(
            settings.rabbitmq_user,
            settings.rabbitmq_pass
        )
        parameters = pika.ConnectionParameters(
            host=settings.rabbitmq_host,
            port=settings.rabbitmq_port,
            credentials=credentials
        )
        _connection = pika.BlockingConnection(parameters)
        return _connection


def get_channel():
    """获取 RabbitMQ 通道"""
    conn = get_connection()
    return conn.channel()
