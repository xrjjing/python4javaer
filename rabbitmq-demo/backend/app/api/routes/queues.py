"""队列相关 API"""
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import List
import pika

from app.services.queue_client import get_queue_client, BaseQueueClient

router = APIRouter(prefix="/queues", tags=["queues"])


class MessageIn(BaseModel):
    body: str


class MessageOut(BaseModel):
    body: str
    timestamp: str


class MessagesOut(BaseModel):
    messages: List[MessageOut]


class StatsOut(BaseModel):
    message_count: int
    consumer_count: int


@router.post("/{queue_name}/messages")
def send_message(
    queue_name: str,
    msg: MessageIn,
    client: BaseQueueClient = Depends(get_queue_client),
):
    """发送消息到队列"""
    try:
        result = client.send_message(queue_name, msg.body)
        return {"status": "ok", "message": result}
    except pika.exceptions.AMQPConnectionError:
        raise HTTPException(status_code=503, detail="RabbitMQ unavailable")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{queue_name}/messages", response_model=MessagesOut)
def get_messages(
    queue_name: str,
    limit: int = Query(10, ge=1, le=100),
    client: BaseQueueClient = Depends(get_queue_client),
):
    """从队列获取消息"""
    try:
        msgs = client.get_messages(queue_name, limit)
        return {"messages": msgs}
    except pika.exceptions.AMQPConnectionError:
        raise HTTPException(status_code=503, detail="RabbitMQ unavailable")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{queue_name}/stats", response_model=StatsOut)
def get_stats(
    queue_name: str,
    client: BaseQueueClient = Depends(get_queue_client),
):
    """获取队列统计信息"""
    try:
        return client.get_stats(queue_name)
    except pika.exceptions.AMQPConnectionError:
        raise HTTPException(status_code=503, detail="RabbitMQ unavailable")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
