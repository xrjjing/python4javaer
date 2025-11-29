"""
角色与权限管理路由：
- 创建角色 / 权限
- 列出角色 / 权限
- 为角色分配权限
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
    """创建角色。"""
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
    """列出角色及其权限。"""
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
    """创建权限。"""
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
    """列出权限列表。"""
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
    """为角色分配权限。"""
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

