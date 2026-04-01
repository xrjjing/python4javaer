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
        # base_url 默认指向 backend_user_order_service，便于本仓库本地直连联调。
        self.base_url = base_url or str(settings.backend_service_base_url)

    def _handle_response(self, resp: httpx.Response) -> Dict[str, Any]:
        """
        处理 HTTP 响应，统一错误检测与解析。

        这是网关和下游服务之间的“响应边界”：
        - 下游状态码异常 -> 统一转成 BackendServiceError
        - 下游返回非 JSON -> 统一转成 BackendServiceError
        """
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
        """
        调用后端服务创建订单并返回标准化结构。

        排查建议：
        - 如果 gateway.py 能进来但下游报 502，优先看这里
        - 如果下游接口其实成功了，但网关仍报数据结构异常，也先看这里的 OrderOut 校验
        """
        url = f"{self.base_url}/api/orders"
        payload = order_in.dict()
        with httpx.Client(trust_env=False) as client:
            data = self._handle_response(client.post(url, json=payload, timeout=5.0))
        try:
            return OrderOut(**data)
        except ValidationError as exc:
            raise BackendServiceError("后端服务返回数据结构不符合预期") from exc
