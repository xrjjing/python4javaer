"""
认证路由。

前端真实上游：
- login.html -> POST /auth/login
- login.html / admin.html -> GET /auth/me
- admin.html -> POST /auth/logout

下游依赖：
- security.py：密码与 JWT
- dependencies.py：当前用户与 token payload
- log_audit_client.py：登录 / 登出审计上报
"""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import models, schemas, security
from ..database import get_db
from ..dependencies import get_current_user, get_token_payload
from ..log_audit_client import log_audit_client

router = APIRouter(prefix="/auth", tags=["auth"])


# login.html 提交用户名密码后的第一个后端入口。
@router.post("/login", response_model=schemas.APIResponse[schemas.Token])
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    用户登录接口（OAuth2 Password 流）。

    这是 login.html 的第一跳后端入口：
    login-form submit -> /auth/login -> create_access_token() -> 返回 accessToken
    """
    # 第一步：按用户名查用户，再校验密码哈希。
    user = (
        db.query(models.User)
        .filter(models.User.username == form_data.username)
        .first()
    )
    # 第二步：校验密码哈希。
    if not user or not security.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名或密码错误",
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="用户已被禁用")

    # 第二步：签发 JWT，供 admin.html / 其他受保护页面后续复用。
    access_token = security.create_access_token(
        subject=user.id,
        username=user.username,
        is_superuser=user.is_superuser,
    )
    token = schemas.Token(access_token=access_token)
    # 上报登录成功的审计日志（失败时静默忽略）
    client_host = request.client.host if request.client else None
    log_audit_client.send_log(
        {
            "actor": user.username,
            "action": "login",
            "resource": "user",
            "source_service": "rbac",
            "ip": client_host,
            "detail": "用户登录成功",
        }
    )
    return schemas.APIResponse(code=schemas.ErrorCode.OK, message="登录成功", data=token)


# login.html 登录成功后的二次请求入口：admin.html 也会复用它确认当前登录用户。
@router.get("/me", response_model=schemas.APIResponse[schemas.UserOut])
def read_me(current_user: models.User = Depends(get_current_user)):
    """
    获取当前登录用户信息。

    这个接口是前端判断“当前是谁、是不是超管、要不要进后台”的关键依据。
    """
    return schemas.APIResponse(code=schemas.ErrorCode.OK, message="获取成功", data=current_user)


# admin.html 退出登录入口。
@router.post("/logout", response_model=schemas.APIResponse[dict])
def logout(
    request: Request,
    current_user: models.User = Depends(get_current_user),
    payload = Depends(get_token_payload),
):
    """
    登出接口：
    - 并不会“销毁” JWT（JWT 本身不可撤回），
    - 而是将当前 Token 的 jti 加入黑名单（需要在 get_current_user 中检查）。

    这里使用 get_token_payload 依赖解析当前 Token 的 payload，
    并将 jti 加入黑名单，在后续请求中使该 Token 失效。
    """
    # 将当前 Token 放入黑名单直到过期
    security.token_blacklist.add(payload.jti, payload.exp)

    # 上报登出操作的审计日志（失败时静默忽略）
    client_host = request.client.host if request.client else None
    log_audit_client.send_log(
        {
            "actor": current_user.username,
            "action": "logout",
            "resource": "user",
            "source_service": "rbac",
            "ip": client_host,
            "detail": "用户登出成功",
        }
    )

    return schemas.APIResponse(
        code=schemas.ErrorCode.OK,
        message="登出成功",
        data={"username": current_user.username},
    )
