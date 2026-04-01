"""
角色与权限业务服务层。

职责：
- 管理 Role / Permission 的创建与关联；
- 对外提供 router 可直接调用的高层接口。

上游：roles.py
下游：role_repository.py / permission_repository.py
"""

from __future__ import annotations

from typing import List

from sqlalchemy.orm import Session

from .. import models, schemas
from ..repositories import role_repository, permission_repository


def create_role(db: Session, role_in: schemas.RoleCreate) -> models.Role:
    """
    创建角色。

    若角色名已存在，抛出 ValueError。
    """
    # 角色名在业务语义上要求唯一。
    existing = role_repository.get_role_by_name(db, role_in.name)
    if existing:
        raise ValueError("角色名已存在")

    role = models.Role(name=role_in.name, description=role_in.description)
    return role_repository.save_role(db, role)


def list_roles(db: Session) -> List[models.Role]:
    """列出所有角色。"""
    return role_repository.list_roles(db)


def create_permission(
    db: Session,
    perm_in: schemas.PermissionCreate,
) -> models.Permission:
    """
    创建权限。

    若权限 code 已存在，抛出 ValueError。
    """
    # 权限 code 是前后端共同使用的稳定标识，因此也要求唯一。
    existing = permission_repository.get_permission_by_code(db, perm_in.code)
    if existing:
        raise ValueError("权限 code 已存在")

    perm = models.Permission(
        code=perm_in.code,
        name=perm_in.name,
        description=perm_in.description,
    )
    return permission_repository.save_permission(db, perm)


def list_permissions(db: Session) -> List[models.Permission]:
    """列出所有权限。"""
    return permission_repository.list_permissions(db)


def assign_permissions_to_role(
    db: Session,
    role_id: int,
    permission_ids: list[int],
) -> models.Role:
    """
    为角色分配权限（覆盖式）。

    若角色不存在或存在无效权限 ID，抛出 ValueError。
    """
    # 先确保角色存在，再做权限覆盖写入。
    role = role_repository.get_role_by_id(db, role_id)
    if not role:
        raise ValueError("角色不存在")

    # 把 permission_ids 批量转换成权限实体，并校验数量是否一致。
    perms = (
        db.query(models.Permission)
        .filter(models.Permission.id.in_(permission_ids))
        .all()
        if permission_ids
        else []
    )
    if len(perms) != len(permission_ids):
        raise ValueError("存在无效权限 ID")

    # 覆盖式写入：角色最新权限集合以当前请求为准。
    role.permissions = perms
    return role_repository.save_role(db, role)

