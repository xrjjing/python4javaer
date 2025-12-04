"""Gateway Router 层测试（使用依赖覆盖 Mock Client）。"""

import pytest
from fastapi.testclient import TestClient

from app.client_backend_service import BackendServiceError
from app.dependencies import (
    get_backend_client,
    get_current_user,
    get_log_detective_client,
)
from app.log_detective_client import LogDetectiveServiceError
from app.main import app
from app.schemas import OrderCreateIn, OrderOut


class MockBackendClient:
    """Mock BackendServiceClient。"""

    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_user(self, user_id: int) -> dict:
        if user_id == 1:
            return {"id": 1, "username": "test_user"}
        raise BackendServiceError(f"用户 {user_id} 不存在")

    def create_order(self, order_in: OrderCreateIn) -> OrderOut:
        if order_in.user_id == 1:
            return OrderOut(
                order_id=123,
                status="CREATED",
                message="订单创建成功",
            )
        raise BackendServiceError("用户不存在")


class MockLogDetectiveClient:
    """Mock LogDetectiveClient。"""

    def __init__(self, should_timeout: bool = False, should_fail: bool = False):
        self.should_timeout = should_timeout
        self.should_fail = should_fail

    async def analyze_logs(self, body: dict) -> dict:
        if self.should_timeout:
            raise LogDetectiveServiceError("日志分析服务超时")
        if self.should_fail:
            raise LogDetectiveServiceError("日志分析服务内部错误")
        return {"summary": "分析完成", "suspicious_ips": ["1.2.3.4"]}


def mock_superuser():
    """Mock 超级管理员用户。"""
    return {"sub": "1", "username": "admin", "is_superuser": True}


def mock_normal_user():
    """Mock 普通用户。"""
    return {"sub": "1", "username": "user", "is_superuser": False}


@pytest.fixture
def client():
    """测试客户端，覆盖依赖。"""
    app.dependency_overrides[get_backend_client] = lambda: MockBackendClient(
        base_url="http://mock"
    )
    app.dependency_overrides[get_current_user] = mock_superuser
    app.dependency_overrides[get_log_detective_client] = lambda: MockLogDetectiveClient()
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def normal_user_client():
    """普通用户测试客户端。"""
    app.dependency_overrides[get_backend_client] = lambda: MockBackendClient(
        base_url="http://mock"
    )
    app.dependency_overrides[get_current_user] = mock_normal_user
    app.dependency_overrides[get_log_detective_client] = lambda: MockLogDetectiveClient()
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def log_detective_timeout_client():
    """日志侦探服务超时场景测试客户端。"""
    app.dependency_overrides[get_backend_client] = lambda: MockBackendClient(
        base_url="http://mock"
    )
    app.dependency_overrides[get_current_user] = mock_superuser
    app.dependency_overrides[get_log_detective_client] = lambda: MockLogDetectiveClient(
        should_timeout=True
    )
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def log_detective_error_client():
    """日志侦探服务内部错误场景测试客户端。"""
    app.dependency_overrides[get_backend_client] = lambda: MockBackendClient(
        base_url="http://mock"
    )
    app.dependency_overrides[get_current_user] = mock_superuser
    app.dependency_overrides[get_log_detective_client] = lambda: MockLogDetectiveClient(
        should_fail=True
    )
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def test_get_user_success(client):
    """正常获取用户信息。"""
    response = client.get("/gateway/backend/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["id"] == 1


def test_get_user_not_found(client):
    """用户不存在时返回 502。"""
    response = client.get("/gateway/backend/users/999")
    assert response.status_code == 502
    assert "不存在" in response.json()["detail"]


def test_create_order_success(client):
    """正常创建订单（超级管理员）。"""
    response = client.post(
        "/gateway/backend/orders",
        json={"user_id": 1, "product_id": 42, "quantity": 2},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["order_id"] == 123


def test_create_order_forbidden_for_normal_user(normal_user_client):
    """普通用户创建订单时返回 403。"""
    response = normal_user_client.post(
        "/gateway/backend/orders",
        json={"user_id": 1, "product_id": 42, "quantity": 2},
    )
    assert response.status_code == 403
    assert "权限不足" in response.json()["detail"]


def test_create_order_invalid_payload(client):
    """请求体格式错误时返回 422。"""
    response = client.post(
        "/gateway/backend/orders",
        json={"invalid": "data"},
    )
    assert response.status_code == 422


def test_analyze_logs_success(client):
    """日志分析成功时返回统一响应结构。"""
    response = client.post(
        "/gateway/log-detective/analyze",
        json={"log_text": "test log"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["summary"] == "分析完成"


def test_analyze_logs_timeout_returns_504(log_detective_timeout_client):
    """日志分析超时时返回 504。"""
    response = log_detective_timeout_client.post(
        "/gateway/log-detective/analyze",
        json={"log_text": "test log"},
    )
    assert response.status_code == 504
    assert "超时" in response.json()["detail"]


def test_analyze_logs_backend_error_returns_502(log_detective_error_client):
    """日志分析服务内部错误时返回 502。"""
    response = log_detective_error_client.post(
        "/gateway/log-detective/analyze",
        json={"log_text": "test log"},
    )
    assert response.status_code == 502
    assert "内部错误" in response.json()["detail"]
