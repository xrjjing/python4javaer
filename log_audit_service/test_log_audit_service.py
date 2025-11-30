"""
log_audit_service 简单测试。

通过 FastAPI TestClient 验证审计日志创建与查询接口的基本行为。
"""

from datetime import datetime, timedelta

from fastapi.testclient import TestClient

from log_audit_service.app.main import app


client = TestClient(app)


def test_create_log_and_list() -> None:
    """创建一条日志并通过查询接口返回。"""
    payload = {
        "actor": "alice",
        "action": "login",
        "resource": "user",
        "source_service": "rbac",
        "ip": "127.0.0.1",
        "detail": "用户 alice 登录成功",
    }
    resp = client.post("/logs", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["id"] >= 1
    assert data["actor"] == "alice"
    assert data["action"] == "login"

    # 使用 actor 过滤查询
    resp_list = client.get("/logs", params={"actor": "alice", "limit": 10})
    assert resp_list.status_code == 200
    logs = resp_list.json()
    assert any(log["id"] == data["id"] for log in logs)


def test_list_logs_with_time_range() -> None:
    """使用时间范围过滤日志列表。"""
    now = datetime.utcnow()
    # 只要接口接受并返回 200 即可，具体数据内容依赖于已有日志
    since = (now - timedelta(days=1)).isoformat()
    until = (now + timedelta(days=1)).isoformat()

    resp = client.get("/logs", params={"since": since, "until": until, "limit": 5})
    assert resp.status_code == 200

