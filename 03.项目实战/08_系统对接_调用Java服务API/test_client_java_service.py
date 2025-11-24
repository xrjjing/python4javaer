"""JavaServiceClient 客户端行为的基础单元测试。

测试目标：
- _handle_response 成功返回 JSON 时的行为；
- _handle_response 收到 HTTP 错误码时是否抛出 JavaServiceError。
"""

from pathlib import Path
from typing import Any, Dict

import sys

import requests


def _import_client():
    """动态导入 client_java_service 模块。"""
    current_dir = Path(__file__).resolve().parent
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))
    import client_java_service  # type: ignore

    return client_java_service


class DummyResponse:
    """用于模拟 requests.Response 的简化版本。"""

    def __init__(
        self,
        status_code: int = 200,
        text: str = "",
        headers: Dict[str, str] | None = None,
        json_data: Any | None = None,
    ) -> None:
        self.status_code = status_code
        self.text = text
        self._json_data = json_data
        self.headers = headers or {"Content-Type": "application/json"}

    def raise_for_status(self) -> None:
        """模拟 requests.Response.raise_for_status。"""
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} {self.text}")

    def json(self) -> Any:
        return self._json_data


def test_handle_response_ok_json() -> None:
    """当返回 200 且是 JSON 时，应正常解析为 Python 对象。"""
    client_mod = _import_client()
    client = client_mod.JavaServiceClient(base_url="http://example.com")

    resp = DummyResponse(
        status_code=200,
        json_data={"id": 1, "name": "Tom"},
    )
    data = client._handle_response(resp)  # type: ignore[arg-type]
    assert isinstance(data, dict)
    assert data["id"] == 1
    assert data["name"] == "Tom"


def test_handle_response_http_error() -> None:
    """当返回 5xx 时，应抛出 JavaServiceError。"""
    client_mod = _import_client()
    client = client_mod.JavaServiceClient(base_url="http://example.com")

    resp = DummyResponse(status_code=500, text="server error")

    try:
        client._handle_response(resp)  # type: ignore[arg-type]
    except client_mod.JavaServiceError as exc:
        # 这里不要求精确消息，只要包含状态码即可
        assert "500" in str(exc)
    else:
        raise AssertionError("预期应抛出 JavaServiceError")

