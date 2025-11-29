"""
Task 相关业务逻辑（Service 层）。

职责：
- 组合 Repository 操作与业务规则；
- 保证用户只能操作自己项目下的任务；
- 对外暴露与路由层对齐的高层接口。
"""

from __future__ import annotations

from typing import List

from sqlalchemy.orm import Session

from .. import models, schemas
from ..repositories import project_repository, task_repository


def list_tasks_for_user_in_project(
    db: Session,
    user: models.User,
    project_id: int,
) -> List[models.Task]:
    """列出当前用户某个项目下的所有任务。"""
    # 先校验项目归属
    project = project_repository.get_project_by_id_for_owner(
        db=db,
        project_id=project_id,
        owner_id=user.id,
    )
    if not project:
        raise ValueError("Project 不存在或不属于当前用户")

    return task_repository.list_tasks_for_project_and_owner(
        db=db,
        project_id=project_id,
        owner_id=user.id,
    )


def create_task_for_user_in_project(
    db: Session,
    user: models.User,
    project_id: int,
    task_in: schemas.TaskCreate,
) -> models.Task:
    """在当前用户的指定项目下创建任务。"""
    project = project_repository.get_project_by_id_for_owner(
        db=db,
        project_id=project_id,
        owner_id=user.id,
    )
    if not project:
        raise ValueError("Project 不存在或不属于当前用户")

    return task_repository.create_task_for_project(
        db=db,
        project_id=project_id,
        title=task_in.title,
        description=task_in.description,
        status=task_in.status,
    )


def update_task_for_user_in_project(
    db: Session,
    user: models.User,
    project_id: int,
    task_id: int,
    task_in: schemas.TaskUpdate,
) -> models.Task:
    """
    更新当前用户某个项目下的任务。

    若项目不存在或任务不属于该项目/用户，抛出 ValueError。
    """
    task = task_repository.get_task_for_owner_in_project(
        db=db,
        task_id=task_id,
        project_id=project_id,
        owner_id=user.id,
    )
    if not task:
        raise ValueError("Task 不存在或不属于当前用户的项目")

    if task_in.title is not None:
        task.title = task_in.title
    if task_in.description is not None:
        task.description = task_in.description
    if task_in.status is not None:
        task.status = task_in.status

    return task_repository.save_task(db, task)


def delete_task_for_user_in_project(
    db: Session,
    user: models.User,
    project_id: int,
    task_id: int,
) -> None:
    """
    删除当前用户某个项目下的任务。

    若项目不存在或任务不属于该项目/用户，抛出 ValueError。
    """
    task = task_repository.get_task_for_owner_in_project(
        db=db,
        task_id=task_id,
        project_id=project_id,
        owner_id=user.id,
    )
    if not task:
        raise ValueError("Task 不存在或不属于当前用户的项目")

    task_repository.delete_task(db, task)

