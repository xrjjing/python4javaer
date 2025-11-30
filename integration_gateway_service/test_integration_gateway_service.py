"""
integration_gateway_service 测试。

包含：
- 应用启动测试；
- 网关路由在依赖覆盖下的基本行为测试。
"""

from fastapi.testclient import TestClient

from integration_gateway_service.app.main import app
from integration_gateway_service.app.dependencies import (
    get_backend_client,
    get_current_user,
)
from integration_gateway_service.app.client_backend_service import BackendServiceError
from integration_gateway_service.app.schemas import OrderOut


class _DummyBackendClient:
    """用于测试的后端服务客户端假实现。"""

    def get_user(self, user_id: int) -> dict:
        return {"id": user_id, "username": "dummy", "full_name": "Dummy User"}

    def create_order(self, order_in) -> OrderOut:
        return OrderOut(
            order_id=123,
            status="CREATED",
            message="测试订单",
            created_at="2024-01-01T00:00:00Z",  # Pydantic 会接受 ISO 字符串
        )


class _ErrorBackendClient:
    """总是抛出错误的后端客户端，用于测试 502 场景。"""

    def get_user(self, user_id: int) -> dict:
        raise BackendServiceError("后端服务异常")

    def create_order(self, order_in) -> OrderOut:
        raise BackendServiceError("后端服务异常")


def _override_current_user_ok():
    """依赖覆盖：模拟已认证用户。"""
    return {"sub": "1", "is_superuser": True}


def _override_current_user_missing_sub():
    """依赖覆盖：模拟 payload 中缺少 sub 字段。"""
    return {}


def test_app_can_start() -> None:
    """验证应用可以正常创建并返回 OpenAPI 文档。"""
    client = TestClient(app)
    resp = client.get("/openapi.json")
    assert resp.status_code == 200
    assert resp.json().get("info", {}).get("title") == "Integration Gateway Service"


def test_gateway_get_user_success() -> None:
    """网关成功代理用户查询接口。"""
    app.dependency_overrides[get_backend_client] = lambda: _DummyBackendClient()
    app.dependency_overrides[get_current_user] = _override_current_user_ok

    client = TestClient(app)
    resp = client.get("/gateway/backend/users/10")
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["data"]["id"] == 10

    app.dependency_overrides.clear()


def test_gateway_create_order_success() -> None:
    """网关成功代理订单创建接口。"""
    app.dependency_overrides[get_backend_client] = lambda: _DummyBackendClient()
    app.dependency_overrides[get_current_user] = _override_current_user_ok

    client = TestClient(app)
    payload = {"product_id": 42, "quantity": 2}
    resp = client.post("/gateway/backend/orders", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["success"] is True
    assert data["data"]["order_id"] == 123

    app.dependency_overrides.clear()


def test_gateway_create_order_missing_sub() -> None:
    """当当前用户信息缺少 sub 字段时应返回 400。"""
    app.dependency_overrides[get_backend_client] = lambda: _DummyBackendClient()
    app.dependency_overrides[get_current_user] = _override_current_user_missing_sub

    client = TestClient(app)
    payload = {"product_id": 42, "quantity": 2}
    resp = client.post("/gateway/backend/orders", json=payload)
    assert resp.status_code == 400

    app.dependency_overrides.clear()


def test_gateway_backend_error_translated_to_502() -> None:
    """当后端服务抛出错误时，网关应返回 502。"""
    app.dependency_overrides[get_backend_client] = lambda: _ErrorBackendClient()
    app.dependency_overrides[get_current_user] = _override_current_user_ok

    client = TestClient(app)
    resp = client.get("/gateway/backend/users/1")
    assert resp.status_code == 502

    app.dependency_overrides.clear()
