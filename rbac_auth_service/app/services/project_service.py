"""
Project 相关业务逻辑（Service 层）。

职责：
- 组合 Repository 操作与业务规则；
- 对外暴露与路由层对齐的高层接口。
"""

from __future__ import annotations

from typing import List

from sqlalchemy.orm import Session

from .. import models, schemas
from ..repositories import project_repository


def list_projects_for_user(db: Session, user: models.User) -> List[models.Project]:
    """列出指定用户的所有项目。"""
    return project_repository.list_projects_by_owner(db, owner_id=user.id)


def create_project_for_user(
    db: Session,
    user: models.User,
    project_in: schemas.ProjectCreate,
) -> models.Project:
    """为指定用户创建项目。"""
    return project_repository.create_project_for_owner(
        db=db,
        owner_id=user.id,
        name=project_in.name,
        description=project_in.description,
    )


def update_project_for_user(
    db: Session,
    user: models.User,
    project_id: int,
    project_in: schemas.ProjectUpdate,
) -> models.Project:
    """
    更新指定用户的项目。

    若不存在或不属于该用户，抛出 ValueError 以由上层转换为 404。
    """
    project = project_repository.get_project_by_id_for_owner(
        db=db,
        project_id=project_id,
        owner_id=user.id,
    )
    if not project:
        raise ValueError("Project 不存在或不属于当前用户")

    if project_in.name is not None:
        project.name = project_in.name
    if project_in.description is not None:
        project.description = project_in.description
    if project_in.status is not None:
        project.status = project_in.status

    return project_repository.save_project(db, project)


def delete_project_for_user(
    db: Session,
    user: models.User,
    project_id: int,
) -> None:
    """
    删除指定用户的项目。

    若不存在或不属于该用户，抛出 ValueError 以由上层转换为 404。
    """
    project = project_repository.get_project_by_id_for_owner(
        db=db,
        project_id=project_id,
        owner_id=user.id,
    )
    if not project:
        raise ValueError("Project 不存在或不属于当前用户")

    project_repository.delete_project(db, project)

