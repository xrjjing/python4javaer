"""
用户业务服务层。

职责：
- 组合 user_repository / role_repository / security；
- 把“创建用户、更新用户、分配角色”等业务规则从 router 中拆出来。

上游：users.py
下游：repositories + security.py
"""

from __future__ import annotations

from typing import List

from sqlalchemy.orm import Session

from .. import models, schemas, security
from ..repositories import user_repository, role_repository


def create_user(db: Session, user_in: schemas.UserCreate) -> models.User:
    """
    创建用户。

    若用户名已存在，抛出 ValueError。
    """
    # 先做业务规则校验：用户名不能重复。
    existing = user_repository.get_user_by_username(db, user_in.username)
    if existing:
        raise ValueError("用户名已存在")

    # 再处理密码哈希，避免把明文密码直接落库。
    hashed_password = security.hash_password(user_in.password)
    user = models.User(
        username=user_in.username,
        hashed_password=hashed_password,
        is_superuser=user_in.is_superuser,
    )
    # 最终统一走 repository 持久化。
    return user_repository.save_user(db, user)


def list_users(db: Session) -> List[models.User]:
    """列出所有用户。"""
    return user_repository.list_users(db)


def update_user(
    db: Session,
    user_id: int,
    user_in: schemas.UserUpdate,
) -> models.User:
    """
    更新用户密码 / 状态 / 超管标记。

    若用户不存在，抛出 ValueError。
    """
    # 先查目标用户；不存在就让 router 转成 404。
    user = user_repository.get_user_by_id(db, user_id)
    if not user:
        raise ValueError("用户不存在")

    if user_in.password:
        user.hashed_password = security.hash_password(user_in.password)
    if user_in.is_active is not None:
        user.is_active = user_in.is_active
    if user_in.is_superuser is not None:
        user.is_superuser = user_in.is_superuser

    return user_repository.save_user(db, user)


def assign_roles_to_user(
    db: Session,
    user_id: int,
    role_ids: list[int],
) -> models.User:
    """
    为用户分配角色（覆盖式）。

    若用户不存在或存在无效角色 ID，抛出 ValueError。
    """
    user = user_repository.get_user_by_id(db, user_id)
    if not user:
        raise ValueError("用户不存在")

    # 这里做“角色 ID -> 角色实体”映射，并保证传入的每个 ID 都真实存在。
    roles = (
        db.query(models.Role)
        .filter(models.Role.id.in_(role_ids))
        .all()
        if role_ids
        else []
    )
    if len(roles) != len(role_ids):
        raise ValueError("存在无效角色 ID")

    # 覆盖式写入：前端提交的新角色集合会直接替换旧集合。
    user.roles = roles
    return user_repository.save_user(db, user)

