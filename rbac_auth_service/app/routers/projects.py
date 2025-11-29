"""
受 RBAC 控制的 Project 示例接口：
- 列表 / 创建 / 更新 / 删除
- 通过 require_permissions 控制访问权限
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..dependencies import get_current_active_user, require_permissions
from ..services import project_service

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get(
    "/",
    response_model=schemas.APIResponse[List[schemas.ProjectOut]],
    dependencies=[Depends(require_permissions("projects:read"))],
)
def list_projects(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """列出当前用户的项目。"""
    projects = project_service.list_projects_for_user(db, current_user)
    return schemas.APIResponse(
        code=schemas.ErrorCode.OK,
        message="获取项目列表成功",
        data=projects,
    )


@router.post(
    "/",
    response_model=schemas.APIResponse[schemas.ProjectOut],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permissions("projects:write"))],
)
def create_project(
    project_in: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """为当前用户创建项目。"""
    project = project_service.create_project_for_user(db, current_user, project_in)
    return schemas.APIResponse(
        code=schemas.ErrorCode.OK,
        message="创建项目成功",
        data=project,
    )


@router.put(
    "/{project_id}",
    response_model=schemas.APIResponse[schemas.ProjectOut],
    dependencies=[Depends(require_permissions("projects:write"))],
)
def update_project(
    project_id: int,
    project_in: schemas.ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """更新当前用户的项目。"""
    try:
        project = project_service.update_project_for_user(
            db=db,
            user=current_user,
            project_id=project_id,
            project_in=project_in,
        )
    except ValueError:
        raise HTTPException(status_code=404, detail="Project 不存在")
    return schemas.APIResponse(
        code=schemas.ErrorCode.OK,
        message="更新项目成功",
        data=project,
    )


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permissions("projects:delete"))],
)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """删除当前用户的项目（需要 projects:delete 权限）。"""
    try:
        project_service.delete_project_for_user(
            db=db,
            user=current_user,
            project_id=project_id,
        )
    except ValueError:
        raise HTTPException(status_code=404, detail="Project 不存在")
    return None

