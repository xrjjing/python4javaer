"""集中放置示例依赖，方便在路由间复用或在测试中覆盖。"""

from typing import Any, Dict, List, TypedDict


class User(TypedDict):
    id: int
    name: str
    email: str


class Product(TypedDict):
    id: int
    title: str
    price: float


FakeDB = Dict[str, List[Dict[str, Any]]]

_FAKE_DB: FakeDB = {
    "users": [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
    ],
    "products": [
        {"id": 1, "title": "Keyboard", "price": 199.0},
        {"id": 2, "title": "Mouse", "price": 99.0},
    ],
}


def get_db() -> FakeDB:
    """
    模拟数据库连接的依赖。
    - 在真实项目里这里会返回 Session/Client。
    - 在测试中可通过 dependency_overrides 覆盖该函数。
    """
    return _FAKE_DB
