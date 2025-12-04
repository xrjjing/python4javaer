"""
下游后端服务客户端封装。

该模块负责与下游 HTTP 服务进行通信，提供更 Pythonic 的调用接口。
下游服务可以是 Python、Java 或其他语言实现的微服务，这里只关心 HTTP 协议本身。
"""

from typing import Any, Dict

import httpx
from pydantic import ValidationError

from .config import settings
from .schemas import OrderCreateIn, OrderOut


class BackendServiceError(Exception):
    """表示调用下游后端服务过程中发生的异常。"""


class BackendServiceClient:
    """通用后端服务客户端封装。"""

    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = base_url or str(settings.backend_service_base_url)

    def _handle_response(self, resp: httpx.Response) -> Dict[str, Any]:
        """处理 HTTP 响应，统一错误检测与解析。"""
        try:
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise BackendServiceError(
                f"调用后端服务失败，状态码：{exc.response.status_code}"
            ) from exc
        try:
            return resp.json()
        except ValueError as exc:
            raise BackendServiceError("后端服务返回了非 JSON 格式的数据") from exc

    def get_user(self, user_id: int) -> Dict[str, Any]:
        """调用后端服务查询用户信息。"""
        url = f"{self.base_url}/api/users/{user_id}"
        with httpx.Client(trust_env=False) as client:
            data = self._handle_response(client.get(url, timeout=5.0))
        return data

    def create_order(self, order_in: OrderCreateIn) -> OrderOut:
        """调用后端服务创建订单并返回标准化结构。"""
        url = f"{self.base_url}/api/orders"
        payload = order_in.dict()
        with httpx.Client(trust_env=False) as client:
            data = self._handle_response(client.post(url, json=payload, timeout=5.0))
        try:
            return OrderOut(**data)
        except ValidationError as exc:
            raise BackendServiceError("后端服务返回数据结构不符合预期") from exc
