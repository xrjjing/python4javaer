"""BackendServiceClient HTTP 层测试。"""

import pytest
import respx
from httpx import Response

from app.client_backend_service import (
    BackendServiceClient,
    BackendServiceError,
)
from app.schemas import OrderCreateIn


@respx.mock
def test_get_user_success():
    """正常获取用户信息。"""
    client = BackendServiceClient(base_url="http://backend")
    respx.get("http://backend/api/users/1").mock(
        return_value=Response(200, json={"id": 1, "username": "test"})
    )

    result = client.get_user(1)
    assert result == {"id": 1, "username": "test"}


@respx.mock
def test_get_user_404_raises_error():
    """后端返回 404 时抛出异常。"""
    client = BackendServiceClient(base_url="http://backend")
    respx.get("http://backend/api/users/999").mock(return_value=Response(404))

    with pytest.raises(BackendServiceError, match="状态码：404"):
        client.get_user(999)


@respx.mock
def test_get_user_500_raises_error():
    """后端返回 500 时抛出异常。"""
    client = BackendServiceClient(base_url="http://backend")
    respx.get("http://backend/api/users/1").mock(return_value=Response(500))

    with pytest.raises(BackendServiceError, match="状态码：500"):
        client.get_user(1)


@respx.mock
def test_get_user_non_json_response_raises_error():
    """后端返回非 JSON 时抛出异常。"""
    client = BackendServiceClient(base_url="http://backend")
    respx.get("http://backend/api/users/1").mock(
        return_value=Response(200, text="not json")
    )

    with pytest.raises(BackendServiceError, match="非 JSON 格式"):
        client.get_user(1)


@respx.mock
def test_create_order_success():
    """正常创建订单。"""
    client = BackendServiceClient(base_url="http://backend")
    respx.post("http://backend/api/orders").mock(
        return_value=Response(
            201,
            json={
                "order_id": 123,
                "status": "CREATED",
                "message": "订单创建成功",
                "created_at": "2024-01-01T00:00:00Z",
            },
        )
    )

    order_in = OrderCreateIn(user_id=1, product_id=42, quantity=2)
    result = client.create_order(order_in)

    assert result.order_id == 123
    assert result.status == "CREATED"


@respx.mock
def test_create_order_invalid_response_structure():
    """后端返回结构不符合预期时抛出异常。"""
    client = BackendServiceClient(base_url="http://backend")
    respx.post("http://backend/api/orders").mock(
        return_value=Response(200, json={"invalid": "data"})
    )

    order_in = OrderCreateIn(user_id=1, product_id=42, quantity=2)
    with pytest.raises(BackendServiceError, match="数据结构不符合预期"):
        client.create_order(order_in)