"""
backend_user_order_service 简单测试。

这里通过 FastAPI TestClient 验证核心接口的基本行为。
"""

from fastapi.testclient import TestClient

from backend_user_order_service.app.main import app


client = TestClient(app)


def test_get_existing_user() -> None:
    """查询已存在用户应返回 200。"""
    resp = client.get("/api/users/1")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == 1
    assert data["username"] == "alice"


def test_get_missing_user() -> None:
    """查询不存在用户应返回 404。"""
    resp = client.get("/api/users/9999")
    assert resp.status_code == 404


def test_create_order() -> None:
    """创建订单应返回 201 且包含订单 ID。"""
    payload = {"user_id": 1, "product_id": 42, "quantity": 3}
    resp = client.post("/api/orders", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["order_id"] >= 1
    assert data["status"] == "CREATED"
    assert "created_at" in data

