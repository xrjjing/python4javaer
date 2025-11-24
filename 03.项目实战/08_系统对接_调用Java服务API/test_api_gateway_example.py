"""FastAPI 网关 api_gateway_example 的基础接口测试。

测试目标：
- 当 Java 客户端返回正常数据时，网关能成功透传并转换格式；
- 当 Java 客户端抛出 JavaServiceError 时，网关会返回 502；
- 当返回数据格式异常时，网关会返回 500。
"""

from pathlib import Path
from typing import Any, Dict, Optional

import sys

from fastapi.testclient import TestClient


def _import_gateway():
    """动态导入 api_gateway_example 模块。"""
    current_dir = Path(__file__).resolve().parent
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))
    import api_gateway_example  # type: ignore

    return api_gateway_example


class FakeJavaClient:
    """用于测试的假 Java 客户端实现。"""

    def __init__(
        self,
        user_data: Dict[int, Dict[str, Any]] | None = None,
        raise_error: bool = False,
        invalid_format: bool = False,
    ) -> None:
        self._user_data = user_data or {}
        self._raise_error = raise_error
        self._invalid_format = invalid_format

    def get_user(self, user_id: int) -> Dict[str, Any]:
        """模拟查询用户信息。"""
        gateway = _import_gateway()
        if self._raise_error:
            raise gateway.JavaServiceError("mock error")
        data: Dict[str, Any] = self._user_data.get(
            user_id, {"id": user_id, "name": "User"}
        )
        if self._invalid_format:
            # 返回非 dict，用于触发「返回格式异常」
            return {"id": "not-int"}  # 仍然是 dict，但内容不符合预期
        return data

    def create_order(
        self, user_id: int, amount: float, comment: Optional[str] = None
    ) -> Dict[str, Any]:
        """模拟创建订单。"""
        gateway = _import_gateway()
        if self._raise_error:
            raise gateway.JavaServiceError("mock error")
        if self._invalid_format:
            # 模拟缺少 id 字段
            return {"userId": user_id, "amount": amount}
        return {"id": 123, "userId": user_id, "amount": amount}


def _create_test_client(fake_client: FakeJavaClient) -> TestClient:
    """构造带有 FakeJavaClient 依赖注入覆盖的 TestClient。"""
    gateway = _import_gateway()
    app = gateway.app

    def override_get_java_client() -> FakeJavaClient:
        return fake_client

    app.dependency_overrides[gateway.get_java_client] = override_get_java_client
    return TestClient(app)


def test_proxy_get_user_success() -> None:
    """正常场景：查询用户信息应返回 200 和统一响应结构。"""
    fake = FakeJavaClient(user_data={1: {"id": 1, "name": "Alice"}})
    client = _create_test_client(fake)

    resp = client.get("/proxy/users/1")
    assert resp.status_code == 200
    body = resp.json()
    # 使用 ApiResponse 模板：code / message / data
    assert body["code"] == 0
    assert body["message"] == "ok"
    assert body["data"]["id"] == 1
    assert body["data"]["name"] == "Alice"


def test_proxy_get_user_java_error() -> None:
    """当底层 Java 客户端抛错时，网关应返回 502。"""
    fake = FakeJavaClient(raise_error=True)
    client = _create_test_client(fake)

    resp = client.get("/proxy/users/1")
    assert resp.status_code == 502
    body = resp.json()
    assert "detail" in body


def test_proxy_create_order_success() -> None:
    """正常场景：创建订单成功返回 200，并按统一响应结构包装 OrderOut。"""
    fake = FakeJavaClient()
    client = _create_test_client(fake)

    resp = client.post(
        "/proxy/orders",
        json={"user_id": 1, "amount": 99.5, "comment": "test"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["code"] == 0
    assert body["message"] == "ok"
    assert body["data"]["id"] == 123
    assert body["data"]["user_id"] == 1
    assert body["data"]["amount"] == 99.5


def test_proxy_create_order_invalid_format() -> None:
    """当 Java 返回数据格式不符合约定时，应返回 500。"""
    fake = FakeJavaClient(invalid_format=True)
    client = _create_test_client(fake)

    resp = client.post(
        "/proxy/orders",
        json={"user_id": 1, "amount": 10.0},
    )
    assert resp.status_code == 500
    body = resp.json()
    assert "detail" in body
