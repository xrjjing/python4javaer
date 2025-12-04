"""端到端冒烟测试（不使用 Mock，验证服务启动和基本路由）。"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """测试客户端。"""
    with TestClient(app) as c:
        yield c


def test_app_starts_successfully(client):
    """验证应用能够成功启动。"""
    assert app is not None
    assert app.title == "Integration Gateway Service"


def test_openapi_docs_accessible(client):
    """验证 OpenAPI 文档可访问。"""
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_json_accessible(client):
    """验证 OpenAPI JSON 可访问。"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert data["info"]["title"] == "Integration Gateway Service"


def test_gateway_routes_registered():
    """验证网关路由已注册。"""
    routes = [route.path for route in app.routes]
    assert "/gateway/backend/users/{user_id}" in routes
    assert "/gateway/backend/orders" in routes
    assert "/gateway/log-detective/analyze" in routes
