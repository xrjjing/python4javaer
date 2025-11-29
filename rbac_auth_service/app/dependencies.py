"""
通用依赖：
- 数据库会话
- 当前用户获取
- RBAC 检查依赖（require_roles / require_permissions）
"""

from __future__ import annotations

from typing import Iterable, List

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from . import models, security
from .database import get_db
from .schemas import TokenPayload, UserOut


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> models.User:
    """
    通过 JWT 获取当前用户。

    - 验证 Token 合法性与是否过期；
    - 检查是否在黑名单（登出后）；
    - 从数据库加载用户信息及其角色、权限。
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭证",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload: TokenPayload = security.decode_token(token)
    except Exception:
        raise credentials_exception

    # 检查黑名单
    if security.token_blacklist.contains(payload.jti):
        raise credentials_exception

    user = db.query(models.User).filter(models.User.id == payload.sub).first()
    if not user or not user.is_active:
        raise credentials_exception
    return user


def get_token_payload(token: str = Depends(oauth2_scheme)) -> TokenPayload:
    """
    仅解析并返回 TokenPayload 的依赖。

    用于登出等需要访问 jti/exp 的场景。
    """
    try:
        payload: TokenPayload = security.decode_token(token)
        return payload
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无法验证凭证",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_active_user(current_user: models.User = Depends(get_current_user)) -> models.User:
    """确保当前用户处于激活状态。"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="用户已被禁用")
    return current_user


def require_superuser(current_user: models.User = Depends(get_current_active_user)) -> models.User:
    """确保当前用户是超级管理员。"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="需要超级管理员权限")
    return current_user


def user_has_any_role(user: models.User, roles: Iterable[str]) -> bool:
    role_names = {r.name for r in user.roles}
    return any(required in role_names for required in roles)


def user_has_any_permission(user: models.User, permissions: Iterable[str]) -> bool:
    # 超管直接放行
    if user.is_superuser:
        return True

    perm_codes = {p.code for role in user.roles for p in role.permissions}
    return any(required in perm_codes for required in permissions)


def require_roles(*role_names: str):
    """
    返回一个依赖，用于要求当前用户具备任意一个指定角色。

    示例：
        @router.get("/admin", dependencies=[Depends(require_roles("admin"))])
    """

    def dependency(current_user: models.User = Depends(get_current_active_user)) -> models.User:
        if current_user.is_superuser:
            return current_user
        if not user_has_any_role(current_user, role_names):
            raise HTTPException(status_code=403, detail="角色不足，拒绝访问")
        return current_user

    return dependency


def require_permissions(*perm_codes: str):
    """
    返回一个依赖，用于要求当前用户具备任意一个指定权限码。

    示例：
        @router.get("/todos", dependencies=[Depends(require_permissions("todos:read"))])
    """

    def dependency(current_user: models.User = Depends(get_current_active_user)) -> models.User:
        if not user_has_any_permission(current_user, perm_codes):
            raise HTTPException(status_code=403, detail="权限不足，拒绝访问")
        return current_user

    return dependency


__all__ = [
    "get_current_user",
    "get_current_active_user",
    "require_superuser",
    "require_roles",
    "require_permissions",
    "get_token_payload",
]
