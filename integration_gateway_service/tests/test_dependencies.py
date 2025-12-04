"""依赖注入函数测试（认证逻辑）。"""

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt

from app.config import settings
from app.dependencies import get_current_user


def test_get_current_user_success():
    """正常解析 JWT 返回 payload。"""
    payload = {"sub": "123", "username": "test", "is_superuser": False}
    token = jwt.encode(payload, settings.rbac_jwt_secret_key, algorithm=settings.rbac_jwt_algorithm)
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)

    result = get_current_user(credentials)
    assert result["sub"] == "123"
    assert result["username"] == "test"


def test_get_current_user_no_credentials():
    """无凭证时返回 401。"""
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(None)
    assert exc_info.value.status_code == 401


def test_get_current_user_invalid_token():
    """无效 JWT 时返回 401。"""
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="invalid.token.here")
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(credentials)
    assert exc_info.value.status_code == 401


def test_get_current_user_missing_sub():
    """payload 缺少 sub 时返回 401。"""
    payload = {"username": "test"}
    token = jwt.encode(payload, settings.rbac_jwt_secret_key, algorithm=settings.rbac_jwt_algorithm)
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(credentials)
    assert exc_info.value.status_code == 401