"""
Task 相关的持久化操作（Repository 层）。
"""

from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import Session

from .. import models


def list_tasks_for_project_and_owner(
    db: Session,
    project_id: int,
    owner_id: int,
) -> List[models.Task]:
    """查询指定用户某个项目下的全部任务。"""
    return (
        db.query(models.Task)
        .join(models.Project)
        .filter(
            models.Task.project_id == project_id,
            models.Project.owner_id == owner_id,
        )
        .all()
    )


def get_task_for_owner_in_project(
    db: Session,
    task_id: int,
    project_id: int,
    owner_id: int,
) -> Optional[models.Task]:
    """根据 ID 查询任务，并确保属于指定用户的指定项目。"""
    return (
        db.query(models.Task)
        .join(models.Project)
        .filter(
            models.Task.id == task_id,
            models.Task.project_id == project_id,
            models.Project.owner_id == owner_id,
        )
        .first()
    )


def create_task_for_project(
    db: Session,
    project_id: int,
    title: str,
    description: Optional[str] = None,
    status: str = "todo",
) -> models.Task:
    """在指定项目下创建任务。"""
    task = models.Task(
        title=title,
        description=description,
        status=status,
        project_id=project_id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def save_task(db: Session, task: models.Task) -> models.Task:
    """保存已修改的任务。"""
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: models.Task) -> None:
    """删除指定任务。"""
    db.delete(task)
    db.commit()

