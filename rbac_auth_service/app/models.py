"""
RBAC 服务 ORM 模型定义。

核心实体：
- User / Role / Permission：支撑登录、授权和后台管理
- Todo / Project / Task：作为受权限控制的示例业务资源

排查建议：
- 接口字段和数据库状态对不上、关联关系异常时，先回到这里确认模型与关系表定义。
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


# 关联表：用户-角色 多对多。
# admin.html 给用户分配角色时，最终会改到这里。
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
)

# 关联表：角色-权限 多对多。
# 角色赋权成功后，权限检查依赖会沿着 User -> Role -> Permission 这条关系链做判断。
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", ForeignKey("permissions.id"), primary_key=True),
)


class User(Base):
    """
    用户模型。

    这是认证链路的核心实体：
    - auth.py 登录时按 username 查询它；
    - dependencies.py 解析 token 后按 id 回查它；
    - users.py / user_service.py 管理它的状态与角色。
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    roles: Mapped[list["Role"]] = relationship(
        "Role",
        secondary=user_roles,
        back_populates="users",
        lazy="joined",
    )

    todos: Mapped[list["Todo"]] = relationship("Todo", back_populates="owner")
    projects: Mapped[list["Project"]] = relationship("Project", back_populates="owner")


class Role(Base):
    """角色模型，主要服务 users.py 里的角色分配与 roles.py 里的角色管理。"""

    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(String(255))

    users: Mapped[list[User]] = relationship(
        "User",
        secondary=user_roles,
        back_populates="roles",
    )
    permissions: Mapped[list["Permission"]] = relationship(
        "Permission",
        secondary=role_permissions,
        back_populates="roles",
        lazy="joined",
    )


class Permission(Base):
    """权限模型，使用 code 唯一标识具体权限点。"""

    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(String(255))

    roles: Mapped[list[Role]] = relationship(
        "Role",
        secondary=role_permissions,
        back_populates="permissions",
    )


class Todo(Base):
    """受 RBAC 控制的示例 TODO。对应 todos.py -> todo_service.py -> todo_repository.py 这条链路。"""

    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    owner: Mapped[User] = relationship("User", back_populates="todos")


class Project(Base):
    """示例项目模型，用于演示 RBAC 控制的业务资源。"""

    __tablename__ = "projects"
    __table_args__ = (
        UniqueConstraint("owner_id", "name", name="uq_project_owner_name"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    owner: Mapped[User] = relationship("User", back_populates="projects")

    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="project")


class Task(Base):
    """项目下的任务模型，用于演示一对多子资源。"""

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(20), default="todo", nullable=False)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    project: Mapped[Project] = relationship("Project", back_populates="tasks")


__all__ = [
    "User",
    "Role",
    "Permission",
    "Todo",
    "Project",
    "Task",
    "user_roles",
    "role_permissions",
]
