"""TODO Web API（FastAPI + SQLite 示例）的基础接口测试。

测试内容：
- 创建 TODO；
- 查询 TODO 列表；
- 更新 TODO 完成状态；
- 删除 TODO。

为避免污染实际数据库，这里使用独立的 SQLite 内存库并通过依赖注入覆盖 get_db。
"""

from typing import Generator

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database import Base, get_db
from app.main import create_app


def _create_test_app() -> TestClient:
    """构造一个使用内存 SQLite 的测试用 FastAPI 应用。"""
    # 创建内存数据库引擎
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )

    # 为测试数据库创建表结构
    Base.metadata.create_all(bind=engine)

    def override_get_db() -> Generator[Session, None, None]:
        """测试环境下的 get_db 覆盖，实现事务会话。"""
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app = create_app()
    app.dependency_overrides[get_db] = override_get_db

    return TestClient(app)


def test_todo_crud_flow() -> None:
    """完整 CRUD 流程测试：创建 → 查询 → 更新 → 删除。"""
    client = _create_test_app()

    # 1. 创建 TODO
    resp = client.post("/todos/", json={"title": "学习 FastAPI"})
    assert resp.status_code == 201
    created = resp.json()
    todo_id = created["id"]
    assert created["title"] == "学习 FastAPI"
    assert created["completed"] is False

    # 2. 查询列表应该包含刚创建的 TODO
    resp = client.get("/todos/")
    assert resp.status_code == 200
    items = resp.json()
    assert any(item["id"] == todo_id for item in items)

    # 3. 更新完成状态
    resp = client.put(
        f"/todos/{todo_id}", json={"completed": True}
    )
    assert resp.status_code == 200
    updated = resp.json()
    assert updated["completed"] is True

    # 4. 删除 TODO
    resp = client.delete(f"/todos/{todo_id}")
    assert resp.status_code == 204

    # 再次查询时不应再包含该 TODO
    resp = client.get("/todos/")
    ids = [item["id"] for item in resp.json()]
    assert todo_id not in ids

