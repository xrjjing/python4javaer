from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_ok() -> None:
    """health 路由应返回最简单的 ok 字段。"""
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_list_users() -> None:
    """用户列表应返回两个示例对象。"""
    resp = client.get("/users")
    assert resp.status_code == 200
    body = resp.json()
    assert isinstance(body, list)
    assert len(body) == 2
    assert body[0]["name"] == "Alice"


def test_get_single_user() -> None:
    """根据 ID 查找用户应命中 Alice。"""
    resp = client.get("/users/1")
    assert resp.status_code == 200
    assert resp.json()["email"] == "alice@example.com"


def test_user_not_found() -> None:
    """不存在的用户 ID 应返回 404。"""
    resp = client.get("/users/999")
    assert resp.status_code == 404
    assert "not found" in resp.json()["detail"]


def test_list_products() -> None:
    """商品列表应返回两个对象。"""
    resp = client.get("/products")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_get_single_product() -> None:
    """根据 ID 查找商品应命中 Keyboard。"""
    resp = client.get("/products/1")
    assert resp.status_code == 200
    assert resp.json()["title"] == "Keyboard"
