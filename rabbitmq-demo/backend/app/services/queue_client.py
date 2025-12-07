"""队列客户端抽象"""
from abc import ABC, abstractmethod
from typing import List
from collections import defaultdict, deque
import pika
import json
from datetime import datetime

from app.core.rabbit import get_channel
from app.core.config import settings


class BaseQueueClient(ABC):
    """队列客户端基类"""

    @abstractmethod
    def send_message(self, queue: str, body: str) -> dict:
        """发送消息"""
        pass

    @abstractmethod
    def get_messages(self, queue: str, limit: int = 10) -> List[dict]:
        """获取消息"""
        pass

    @abstractmethod
    def get_stats(self, queue: str) -> dict:
        """获取队列统计"""
        pass


class RabbitMQQueueClient(BaseQueueClient):
    """真实 RabbitMQ 客户端"""

    def send_message(self, queue: str, body: str) -> dict:
        ch = get_channel()
        ch.queue_declare(queue=queue, durable=True)

        message_data = {
            "body": body,
            "timestamp": datetime.now().isoformat()
        }

        ch.basic_publish(
            exchange="",
            routing_key=queue,
            body=json.dumps(message_data),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        return message_data

    def get_messages(self, queue: str, limit: int = 10) -> List[dict]:
        ch = get_channel()
        ch.queue_declare(queue=queue, durable=True)
        messages = []
        for _ in range(limit):
            method, properties, body = ch.basic_get(queue=queue, auto_ack=False)
            if method is None:
                break
            try:
                msg_data = json.loads(body.decode("utf-8"))
                messages.append(msg_data)
            except (json.JSONDecodeError, UnicodeDecodeError):
                messages.append({"body": body.decode("utf-8", errors="replace"), "timestamp": ""})
            finally:
                ch.basic_ack(delivery_tag=method.delivery_tag)
        return messages

    def get_stats(self, queue: str) -> dict:
        ch = get_channel()
        result = ch.queue_declare(queue=queue, passive=True)
        return {
            "message_count": result.method.message_count,
            "consumer_count": result.method.consumer_count
        }


class MockQueueClient(BaseQueueClient):
    """Mock 队列客户端（内存模拟）"""

    def __init__(self):
        self._queues = defaultdict(deque)

    def send_message(self, queue: str, body: str) -> dict:
        message_data = {
            "body": body,
            "timestamp": datetime.now().isoformat()
        }
        self._queues[queue].append(message_data)
        return message_data

    def get_messages(self, queue: str, limit: int = 10) -> List[dict]:
        q = self._queues[queue]
        messages = []
        for _ in range(min(limit, len(q))):
            messages.append(q.popleft())
        return messages

    def get_stats(self, queue: str) -> dict:
        q = self._queues[queue]
        return {
            "message_count": len(q),
            "consumer_count": 0
        }


# 全局单例
_mock_client = MockQueueClient()


def get_queue_client() -> BaseQueueClient:
    """根据配置返回对应的队列客户端"""
    if settings.app_mode == "real":
        return RabbitMQQueueClient()
    return _mock_client
