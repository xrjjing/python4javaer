"""
用户管理路由。

前端真实上游：
- admin.html 的用户面板、创建用户按钮、启停用户按钮

下游依赖：
- user_service.py：用户创建、更新、角色分配
- require_superuser()：限制只有超管能操作
- log_audit_client.py：记录关键管理动作
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..dependencies import require_superuser
from ..services import user_service
from ..log_audit_client import log_audit_client

router = APIRouter(prefix="/users", tags=["users"])


# 创建用户入口：admin.html 的 “+ Create User” 按钮最终会到这里。
@router.post(
    "/",
    response_model=schemas.APIResponse[schemas.UserOut],
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user_in: schemas.UserCreate,
    db: Session = Depends(get_db),
    request: Request = None,
    current_user: models.User = Depends(require_superuser),
):
    """
    创建用户（仅超级管理员）。

    调用链：admin.html -> create_user() -> user_service.create_user() -> user_repository.save_user()
    """
    try:
        user = user_service.create_user(db, user_in)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    # 上报创建用户的审计日志
    client_host = request.client.host if request and request.client else None
    log_audit_client.send_log(
        {
            "actor": current_user.username,
            "action": "create_user",
            "resource": "user",
            "source_service": "rbac",
            "ip": client_host,
            "detail": f"创建用户 {user.username}",
        }
    )

    return schemas.APIResponse(
        code=schemas.ErrorCode.OK, message="创建用户成功", data=user
    )


# 用户列表入口：admin.html 的 Users 面板切到激活状态时会请求这里。
@router.get(
    "/",
    response_model=schemas.APIResponse[List[schemas.UserOut]],
)
def list_users(
    db: Session = Depends(get_db),
    request: Request = None,
    current_user: models.User = Depends(require_superuser),
):
    """
    列出所有用户（仅超级管理员）。

    这是 admin.html 打开 Users 面板时最常进入的读取接口。
    """
    users = user_service.list_users(db)

    client_host = request.client.host if request and request.client else None
    log_audit_client.send_log(
        {
            "actor": current_user.username,
            "action": "list_users",
            "resource": "user",
            "source_service": "rbac",
            "ip": client_host,
            "detail": "查看用户列表",
        }
    )

    return schemas.APIResponse(
        code=schemas.ErrorCode.OK, message="获取用户列表成功", data=users
    )


# 用户更新入口：admin.html 的启停用户按钮会走这里。
@router.patch(
    "/{user_id}",
    response_model=schemas.APIResponse[schemas.UserOut],
)
def update_user(
    user_id: int,
    user_in: schemas.UserUpdate,
    db: Session = Depends(get_db),
    request: Request = None,
    current_user: models.User = Depends(require_superuser),
):
    """
    更新用户密码 / 状态 / 超管标记。

    若前端能点按钮但更新不生效，先看这里，再看 user_service.update_user()。
    """
    try:
        user = user_service.update_user(db, user_id=user_id, user_in=user_in)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    client_host = request.client.host if request and request.client else None
    log_audit_client.send_log(
        {
            "actor": current_user.username,
            "action": "update_user",
            "resource": "user",
            "source_service": "rbac",
            "ip": client_host,
            "detail": f"更新用户 {user_id}",
        }
    )

    return schemas.APIResponse(
        code=schemas.ErrorCode.OK, message="更新用户成功", data=user
    )


# 用户角色分配入口：当前前端未直接暴露复杂表单，但后端能力已经在这里。
@router.post(
    "/{user_id}/roles",
    response_model=schemas.APIResponse[schemas.UserOut],
)
def assign_roles_to_user(
    user_id: int,
    req: schemas.AssignRolesRequest,
    db: Session = Depends(get_db),
    request: Request = None,
    current_user: models.User = Depends(require_superuser),
):
    """
    为指定用户分配角色。

    这是“用户”和“角色”两块数据真正汇合的接口入口。
    """
    try:
        user = user_service.assign_roles_to_user(
            db=db,
            user_id=user_id,
            role_ids=req.role_ids,
        )
    except ValueError as exc:
        msg = str(exc)
        if "不存在" in msg:
            raise HTTPException(status_code=404, detail=msg)
        raise HTTPException(status_code=400, detail=msg)

    client_host = request.client.host if request and request.client else None
    log_audit_client.send_log(
        {
            "actor": current_user.username,
            "action": "assign_roles",
            "resource": "user",
            "source_service": "rbac",
            "ip": client_host,
            "detail": f"为用户 {user_id} 分配角色 {req.role_ids}",
        }
    )

    return schemas.APIResponse(
        code=schemas.ErrorCode.OK, message="分配角色成功", data=user
    )
