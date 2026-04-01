"""
角色 Repository。

职责：
- 封装 Role 的查询与持久化；
- 供 rbac_service / user_service 复用。
"""

from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import Session

from .. import models


def get_role_by_name(db: Session, name: str) -> Optional[models.Role]:
    """根据角色名获取角色。"""
    return db.query(models.Role).filter(models.Role.name == name).first()


def get_role_by_id(db: Session, role_id: int) -> Optional[models.Role]:
    """根据 ID 获取角色。"""
    return db.query(models.Role).filter(models.Role.id == role_id).first()


def list_roles(db: Session) -> List[models.Role]:
    """列出所有角色。"""
    return db.query(models.Role).all()


def save_role(db: Session, role: models.Role) -> models.Role:
    """保存角色实体。提交并 refresh 后，调用方能拿到包含最新权限关联的对象。"""
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

