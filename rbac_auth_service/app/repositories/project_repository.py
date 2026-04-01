"""
Project Repository。

职责：
- 处理 Project 的 owner 维度查询、创建、保存和删除；
- 供 project_service / task_service 复用。
"""

from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import Session

from .. import models


def list_projects_by_owner(db: Session, owner_id: int) -> List[models.Project]:
    """查询指定用户的全部项目。"""
    return (
        db.query(models.Project)
        .filter(models.Project.owner_id == owner_id)
        .all()
    )


def get_project_by_id_for_owner(
    db: Session,
    project_id: int,
    owner_id: int,
) -> Optional[models.Project]:
    """根据 ID 查询项目，且确保属于指定用户。"""
    return (
        db.query(models.Project)
        .filter(
            models.Project.id == project_id,
            models.Project.owner_id == owner_id,
        )
        .first()
    )


def create_project_for_owner(
    db: Session,
    owner_id: int,
    name: str,
    description: Optional[str] = None,
) -> models.Project:
    """为指定用户创建项目。"""
    project = models.Project(
        name=name,
        description=description,
        owner_id=owner_id,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def save_project(db: Session, project: models.Project) -> models.Project:
    """保存已修改的项目。"""
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def delete_project(db: Session, project: models.Project) -> None:
    """删除指定项目。"""
    db.delete(project)
    db.commit()

