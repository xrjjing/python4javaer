import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests
from requests import Response


class JavaServiceError(Exception):
    """调用 Java 服务时发生的异常。"""


@dataclass
class JavaServiceClient:
    """
    Java 服务客户端封装。

    在实际项目中，你可以把 base_url 配置成环境变量或配置文件。
    """

    base_url: str
    timeout: int = 5

    @classmethod
    def from_env(cls) -> "JavaServiceClient":
        base_url = os.getenv("JAVA_SERVICE_BASE_URL", "http://localhost:8080")
        return cls(base_url=base_url)

    def _handle_response(self, resp: Response) -> Any:
        """统一处理 HTTP 响应，转换为 Python 对象或抛出异常。"""
        try:
            resp.raise_for_status()
        except requests.HTTPError as exc:
            # 这里可以根据公司规范，解析错误码并转换为统一异常
            raise JavaServiceError(
                f"调用 Java 服务失败：{resp.status_code} {resp.text}"
            ) from exc
        if resp.headers.get("Content-Type", "").startswith("application/json"):
            return resp.json()
        return resp.text

    def get_user(self, user_id: int) -> Dict[str, Any]:
        """调用 Java 服务查询用户信息。"""
        url = f"{self.base_url}/api/users/{user_id}"
        resp = requests.get(url, timeout=self.timeout)
        data = self._handle_response(resp)
        if not isinstance(data, dict):
            raise JavaServiceError("用户接口返回格式异常")
        return data

    def create_order(
        self, user_id: int, amount: float, comment: Optional[str] = None
    ) -> Dict[str, Any]:
        """调用 Java 服务创建订单。"""
        url = f"{self.base_url}/api/orders"
        payload: Dict[str, Any] = {
            "userId": user_id,
            "amount": amount,
        }
        if comment:
            payload["comment"] = comment
        resp = requests.post(url, json=payload, timeout=self.timeout)
        data = self._handle_response(resp)
        if not isinstance(data, dict):
            raise JavaServiceError("订单接口返回格式异常")
        return data

