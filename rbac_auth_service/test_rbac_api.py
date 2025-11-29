"""
RBAC 示例基础测试：
- 初始化数据库中的用户/角色/权限
- 验证登录与权限控制是否生效

说明：
- 为了保持示例简单，这里的测试使用 SQLite，并直接操作数据库初始化数据；
- 若要在你的环境中接入 MySQL / Redis，可参考本测试中的调用流程做手工验证。
"""

from __future__ import annotations

from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database import Base, get_db
from app.main import create_app
from app import models, security


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_rbac.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db() -> Generator[Session, None, None]:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """创建测试数据库表。"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def client() -> TestClient:
    app = create_app()
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


def init_rbac_data(db: Session) -> None:
    """初始化一个 admin 用户、基本角色和权限。"""
    # 创建权限
    perm_todo_read = models.Permission(code="todos:read", name="读取 TODO")
    perm_todo_write = models.Permission(code="todos:write", name="创建/更新 TODO")
    perm_todo_delete = models.Permission(code="todos:delete", name="删除 TODO")
    perm_project_read = models.Permission(code="projects:read", name="读取项目")
    perm_project_write = models.Permission(code="projects:write", name="创建/更新项目")
    perm_project_delete = models.Permission(code="projects:delete", name="删除项目")
    perm_task_read = models.Permission(code="tasks:read", name="读取任务")
    perm_task_write = models.Permission(code="tasks:write", name="创建/更新任务")
    perm_task_delete = models.Permission(code="tasks:delete", name="删除任务")
    db.add_all(
        [
            perm_todo_read,
            perm_todo_write,
            perm_todo_delete,
            perm_project_read,
            perm_project_write,
            perm_project_delete,
            perm_task_read,
            perm_task_write,
            perm_task_delete,
        ]
    )

    # 创建角色
    role_admin = models.Role(name="admin", description="管理员")
    role_user = models.Role(name="user", description="普通用户")
    role_admin.permissions = [
        perm_todo_read,
        perm_todo_write,
        perm_todo_delete,
        perm_project_read,
        perm_project_write,
        perm_project_delete,
        perm_task_read,
        perm_task_write,
        perm_task_delete,
    ]
    role_user.permissions = [
        perm_todo_read,
        perm_todo_write,
        perm_project_read,
        perm_project_write,
        perm_task_read,
        perm_task_write,
    ]
    db.add_all([role_admin, role_user])

    # 创建用户
    admin = models.User(
        username="admin",
        hashed_password=security.hash_password("admin123"),
        is_superuser=True,
    )
    normal = models.User(
        username="alice",
        hashed_password=security.hash_password("alice123"),
    )
    normal.roles = [role_user]
    db.add_all([admin, normal])
    db.commit()


@pytest.fixture
def seeded_db() -> Generator[Session, None, None]:
    db = TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    init_rbac_data(db)
    try:
        yield db
    finally:
        db.close()


def login_and_get_token(client: TestClient, username: str, password: str) -> str:
    resp = client.post(
        "/auth/login",
        data={"username": username, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["code"] == "OK"
    return body["data"]["access_token"]


def test_admin_can_manage_users(client: TestClient, seeded_db: Session):
    token = login_and_get_token(client, "admin", "admin123")

    # 管理员创建新用户
    resp = client.post(
        "/users/",
        json={"username": "bob", "password": "bob123", "is_superuser": False},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 201, resp.text

    # 管理员列出用户
    resp = client.get("/users/", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    users = resp.json()["data"]
    assert any(u["username"] == "bob" for u in users)


def test_normal_user_cannot_manage_users(client: TestClient, seeded_db: Session):
    token = login_and_get_token(client, "alice", "alice123")

    resp = client.get("/users/", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 403


def test_user_todo_rbac(client: TestClient, seeded_db: Session):
    # 普通用户登录
    token = login_and_get_token(client, "alice", "alice123")
    headers = {"Authorization": f"Bearer {token}"}

    # 创建 TODO（有 todos:write）
    resp = client.post("/todos/", json={"title": "task1", "completed": False}, headers=headers)
    assert resp.status_code == 201, resp.text
    todo_id = resp.json()["data"]["id"]

    # 获取 TODO 列表（有 todos:read）
    resp = client.get("/todos/", headers=headers)
    assert resp.status_code == 200
    todos = resp.json()["data"]
    assert len(todos) == 1
    assert todos[0]["id"] == todo_id


def test_user_project_rbac(client: TestClient, seeded_db: Session):
    """验证普通用户对 Project 的权限控制。"""
    token = login_and_get_token(client, "alice", "alice123")
    headers = {"Authorization": f"Bearer {token}"}

    # 创建 Project（有 projects:write）
    resp = client.post(
        "/projects/",
        json={"name": "demo-project", "description": "示例项目"},
        headers=headers,
    )
    assert resp.status_code == 201, resp.text
    project_id = resp.json()["data"]["id"]

    # 获取 Project 列表（有 projects:read）
    resp = client.get("/projects/", headers=headers)
    assert resp.status_code == 200
    projects = resp.json()["data"]
    assert len(projects) == 1
    assert projects[0]["id"] == project_id

    # 更新 Project（有 projects:write）
    resp = client.put(
        f"/projects/{project_id}",
        json={"description": "更新后的描述"},
        headers=headers,
    )
    assert resp.status_code == 200
    assert resp.json()["data"]["description"] == "更新后的描述"


def test_user_task_rbac(client: TestClient, seeded_db: Session):
    """验证普通用户在项目下对 Task 的权限控制。"""
    token = login_and_get_token(client, "alice", "alice123")
    headers = {"Authorization": f"Bearer {token}"}

    # 先创建一个 Project，后续 Task 都挂在此项目下
    resp = client.post(
        "/projects/",
        json={"name": "demo-project", "description": "示例项目"},
        headers=headers,
    )
    assert resp.status_code == 201, resp.text
    project_id = resp.json()["data"]["id"]

    # 创建 Task（有 tasks:write）
    resp = client.post(
        f"/projects/{project_id}/tasks/",
        json={"title": "task-1", "description": "示例任务"},
        headers=headers,
    )
    assert resp.status_code == 201, resp.text
    task_id = resp.json()["data"]["id"]

    # 获取 Task 列表（有 tasks:read）
    resp = client.get(f"/projects/{project_id}/tasks/", headers=headers)
    assert resp.status_code == 200
    tasks = resp.json()["data"]
    assert len(tasks) == 1
    assert tasks[0]["id"] == task_id

    # 更新 Task（有 tasks:write）
    resp = client.put(
        f"/projects/{project_id}/tasks/{task_id}",
        json={"status": "done"},
        headers=headers,
    )
    assert resp.status_code == 200
    assert resp.json()["data"]["status"] == "done"


def test_logout_revokes_token(client: TestClient, seeded_db: Session):
    """登出后，同一 Token 不应再能访问受保护接口。"""
    token = login_and_get_token(client, "alice", "alice123")
    headers = {"Authorization": f"Bearer {token}"}

    # 登出
    resp = client.post("/auth/logout", headers=headers)
    assert resp.status_code == 200

    # 再次访问受保护接口应返回 401
    resp = client.get("/auth/me", headers=headers)
    assert resp.status_code == 401
