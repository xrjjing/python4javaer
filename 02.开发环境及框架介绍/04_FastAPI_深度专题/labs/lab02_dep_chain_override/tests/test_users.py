# tests/test_users.py
"""
依赖覆盖测试：使用内存 SQLite 替换真实数据库

关键技术点：
1. 创建测试专用的内存数据库 Engine
2. 使用 app.dependency_overrides 覆盖依赖链
3. 测试 CRUD 不触碰真实数据库

Java 对比：
- @MockBean 替换 Repository
- @DataJpaTest 使用内嵌数据库
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import create_app
from app.models import Base
from app.db import get_session
from app.config import Settings, get_settings


# === 测试配置 ===

# 1. 创建测试专用的内存 SQLite Engine
TEST_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(
    TEST_DATABASE_URL,
    future=True,
    connect_args={"check_same_thread": False},
    echo=True,  # 打印 SQL 便于调试
)
TestingSessionLocal = sessionmaker(bind=test_engine, autoflush=False, autocommit=False, future=True)


# 2. 覆盖 Settings 依赖
def override_get_settings() -> Settings:
    """返回测试配置：使用内存数据库"""
    return Settings(database_url=TEST_DATABASE_URL, echo_sql=True)


# 3. 覆盖 Session 依赖
def override_get_session():
    """返回测试 Session：指向内存数据库"""
    db = TestingSessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# === Fixtures ===

@pytest.fixture(scope="function")
def client():
    """
    每个测试函数创建独立的客户端和数据库
    确保测试隔离，互不影响

    关键点：
    1. create_app(init_db=False) 禁用生产数据库初始化
    2. 手动在测试 Engine 上创建表
    3. dependency_overrides 替换依赖
    """
    # 在测试 Engine 上创建表
    Base.metadata.create_all(bind=test_engine)

    # 创建应用并禁用生产数据库初始化
    app = create_app(init_db=False)

    # 覆盖依赖：指向内存数据库
    app.dependency_overrides[get_settings] = override_get_settings
    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as c:
        yield c

    # 清理：删除所有表
    Base.metadata.drop_all(bind=test_engine)


# === 测试用例 ===

class TestUserCRUD:
    """用户 CRUD 测试"""

    def test_create_user(self, client):
        """测试创建用户"""
        response = client.post("/users", json={
            "name": "Alice",
            "email": "alice@example.com"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Alice"
        assert data["email"] == "alice@example.com"
        assert "id" in data

    def test_create_user_duplicate_email(self, client):
        """测试重复邮箱应返回 400"""
        client.post("/users", json={"name": "Alice", "email": "dup@example.com"})
        response = client.post("/users", json={"name": "Bob", "email": "dup@example.com"})
        assert response.status_code == 400
        assert "邮箱已被使用" in response.json()["detail"]

    def test_list_users(self, client):
        """测试获取用户列表"""
        # 先创建几个用户
        client.post("/users", json={"name": "User1", "email": "u1@example.com"})
        client.post("/users", json={"name": "User2", "email": "u2@example.com"})

        response = client.get("/users")
        assert response.status_code == 200
        users = response.json()
        assert len(users) == 2

    def test_get_user(self, client):
        """测试获取单个用户"""
        create_resp = client.post("/users", json={"name": "Bob", "email": "bob@example.com"})
        user_id = create_resp.json()["id"]

        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["name"] == "Bob"

    def test_get_user_not_found(self, client):
        """测试获取不存在的用户应返回 404"""
        response = client.get("/users/99999")
        assert response.status_code == 404

    def test_update_user(self, client):
        """测试更新用户"""
        create_resp = client.post("/users", json={"name": "Carol", "email": "carol@example.com"})
        user_id = create_resp.json()["id"]

        response = client.put(f"/users/{user_id}", json={"name": "Carol Updated"})
        assert response.status_code == 200
        assert response.json()["name"] == "Carol Updated"

    def test_delete_user(self, client):
        """测试删除用户"""
        create_resp = client.post("/users", json={"name": "Dave", "email": "dave@example.com"})
        user_id = create_resp.json()["id"]

        # 删除
        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 204

        # 确认已删除
        get_resp = client.get(f"/users/{user_id}")
        assert get_resp.status_code == 404

    def test_delete_user_not_found(self, client):
        """测试删除不存在的用户应返回 404"""
        response = client.delete("/users/99999")
        assert response.status_code == 404


class TestDependencyChain:
    """依赖链测试"""

    def test_dependency_override_works(self, client):
        """验证依赖覆盖生效：使用内存数据库而非真实数据库"""
        # 创建用户
        client.post("/users", json={"name": "Test", "email": "test@example.com"})

        # 验证数据在内存库中
        response = client.get("/users")
        assert response.status_code == 200
        assert len(response.json()) == 1

        # 注意：这里没有创建任何文件数据库（lab02.db）
        # 所有数据都在 sqlite:///:memory: 中

    def test_health_check(self, client):
        """测试健康检查端点"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
