"""
RBAC 服务通用依赖模块。

职责：
- 解析 Bearer Token 并加载当前用户；
- 提供超管、角色、权限等访问控制依赖；
- 让 router 层只声明需要什么权限，而不是自己重复写鉴权逻辑。

真实调用链：
- admin.html / log-detective.html 持有的 accessToken
- -> OAuth2PasswordBearer
- -> get_current_user()
- -> require_superuser() / require_roles() / require_permissions()
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
# 当前仓库里 login.html 提交用户名密码后拿到的 accessToken，
# 后续访问 admin.html / log-detective.html 时，都会通过 Bearer Token 形式回到这里被解析。


# JWT -> 当前用户 的核心解析入口：admin.html 的大多数受保护接口都会先经过这里。
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

    # 黑名单检查：logout 只是把 jti 拉黑，后续请求是否失效就看这里是否命中。
    if security.token_blacklist.contains(payload.jti):
        raise credentials_exception

    user = db.query(models.User).filter(models.User.id == payload.sub).first()
    if not user or not user.is_active:
        raise credentials_exception
    return user


# 只解析 token payload，不查数据库：适合 logout 这类需要 jti/exp 但不需要完整用户对象的场景。
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


# 超管依赖：admin.html 的用户/角色/权限管理大多通过这里把关。
def require_superuser(current_user: models.User = Depends(get_current_active_user)) -> models.User:
    """确保当前用户是超级管理员。"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="需要超级管理员权限")
    return current_user


def user_has_any_role(user: models.User, roles: Iterable[str]) -> bool:
    """判断用户是否命中任意一个角色名。"""
    role_names = {r.name for r in user.roles}
    return any(required in role_names for required in roles)


def user_has_any_permission(user: models.User, permissions: Iterable[str]) -> bool:
    """判断用户是否命中任意一个权限码；超级管理员直接放行。"""
    # 超管直接放行
    if user.is_superuser:
        return True

    perm_codes = {p.code for role in user.roles for p in role.permissions}
    return any(required in perm_codes for required in permissions)


# 角色依赖工厂：返回一个真正供 FastAPI Depends 使用的闭包。
def require_roles(*role_names: str):
    """
    返回一个依赖，用于要求当前用户具备任意一个指定角色。

    示例：
        @router.get("/admin", dependencies=[Depends(require_roles("admin"))])
    """

    def dependency(current_user: models.User = Depends(get_current_active_user)) -> models.User:
        # 这是 router 层真正依赖的闭包；返回 current_user 方便路由继续往下用。
        if current_user.is_superuser:
            return current_user
        if not user_has_any_role(current_user, role_names):
            raise HTTPException(status_code=403, detail="角色不足，拒绝访问")
        return current_user

    return dependency


# 权限依赖工厂：TODO / Project / Task 示例接口会大量复用这里。
def require_permissions(*perm_codes: str):
    """
    返回一个依赖，用于要求当前用户具备任意一个指定权限码。

    示例：
        @router.get("/todos", dependencies=[Depends(require_permissions("todos:read"))])
    """

    def dependency(current_user: models.User = Depends(get_current_active_user)) -> models.User:
        # 这是 router 层真正依赖的闭包；和 require_roles() 的区别在于校验对象是权限码。
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
