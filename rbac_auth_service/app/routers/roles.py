"""
角色与权限管理路由。

前端真实上游：
- admin.html 的角色面板与权限面板

下游依赖：
- rbac_service.py：角色创建、权限创建、角色授权
- require_superuser()：限制高权限管理动作
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..dependencies import require_superuser
from ..services import rbac_service

router = APIRouter(prefix="/rbac", tags=["rbac"])


@router.post(
    "/roles",
    response_model=schemas.APIResponse[schemas.RoleOut],
    status_code=status.HTTP_201_CREATED,
)
def create_role(
    role_in: schemas.RoleCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_superuser),
):
    """创建角色。调用链：admin.html -> create_role() -> rbac_service.create_role() -> role_repository.save_role()."""
    try:
        role = rbac_service.create_role(db, role_in)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return schemas.APIResponse(
        code=schemas.ErrorCode.OK, message="创建角色成功", data=role
    )


@router.get(
    "/roles",
    response_model=schemas.APIResponse[List[schemas.RoleOut]],
)
def list_roles(
    db: Session = Depends(get_db),
    _: models.User = Depends(require_superuser),
):
    """列出角色及其权限。这是 admin.html Roles 面板的主读取接口。"""
    roles = rbac_service.list_roles(db)
    return schemas.APIResponse(
        code=schemas.ErrorCode.OK, message="获取角色列表成功", data=roles
    )


@router.post(
    "/permissions",
    response_model=schemas.APIResponse[schemas.PermissionOut],
    status_code=status.HTTP_201_CREATED,
)
def create_permission(
    perm_in: schemas.PermissionCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_superuser),
):
    """创建权限。新权限会进入 permission_repository，再被角色分配逻辑复用。"""
    try:
        perm = rbac_service.create_permission(db, perm_in)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return schemas.APIResponse(
        code=schemas.ErrorCode.OK, message="创建权限成功", data=perm
    )


@router.get(
    "/permissions",
    response_model=schemas.APIResponse[List[schemas.PermissionOut]],
)
def list_permissions(
    db: Session = Depends(get_db),
    _: models.User = Depends(require_superuser),
):
    """列出权限列表。这是 admin.html Permissions 面板的主读取接口。"""
    perms = rbac_service.list_permissions(db)
    return schemas.APIResponse(
        code=schemas.ErrorCode.OK, message="获取权限列表成功", data=perms
    )


@router.post(
    "/roles/{role_id}/permissions",
    response_model=schemas.APIResponse[schemas.RoleOut],
)
def assign_permissions_to_role(
    role_id: int,
    req: schemas.AssignPermissionsRequest,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_superuser),
):
    """为角色分配权限。这里会把前端传来的 permission_ids 覆盖写入角色权限集合。"""
    try:
        role = rbac_service.assign_permissions_to_role(
            db=db,
            role_id=role_id,
            permission_ids=req.permission_ids,
        )
    except ValueError as exc:
        msg = str(exc)
        if "角色不存在" in msg:
            raise HTTPException(status_code=404, detail=msg)
        raise HTTPException(status_code=400, detail=msg)
    return schemas.APIResponse(
        code=schemas.ErrorCode.OK, message="分配权限成功", data=role
    )
