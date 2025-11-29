"""
认证相关路由：
- /auth/login：用户名密码登录，返回 JWT
- /auth/me：获取当前用户信息
- /auth/logout：可选，将当前 Token 加入黑名单
"""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import models, schemas, security
from ..database import get_db
from ..dependencies import get_current_user, get_token_payload

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=schemas.APIResponse[schemas.Token])
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    用户登录接口（OAuth2 Password 流）。
    """
    user = (
        db.query(models.User)
        .filter(models.User.username == form_data.username)
        .first()
    )
    if not user or not security.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名或密码错误",
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="用户已被禁用")

    access_token = security.create_access_token(
        subject=user.id,
        username=user.username,
        is_superuser=user.is_superuser,
    )
    token = schemas.Token(access_token=access_token)
    return schemas.APIResponse(code=schemas.ErrorCode.OK, message="登录成功", data=token)


@router.get("/me", response_model=schemas.APIResponse[schemas.UserOut])
def read_me(current_user: models.User = Depends(get_current_user)):
    """获取当前登录用户信息。"""
    return schemas.APIResponse(code=schemas.ErrorCode.OK, message="获取成功", data=current_user)


@router.post("/logout", response_model=schemas.APIResponse[dict])
def logout(
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
    return schemas.APIResponse(
        code=schemas.ErrorCode.OK,
        message="登出成功",
        data={"username": current_user.username},
    )
