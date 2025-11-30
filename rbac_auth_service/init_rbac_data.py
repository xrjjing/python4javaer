#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RBAC 示例数据初始化脚本

用途：
- 为 RBAC 示例服务创建基础用户 / 角色 / 权限数据；
- 默认会创建：
  - 超级管理员：用户名 admin，密码 admin123
  - 普通用户：用户名 alice，密码 alice123
  - 角色：admin、user
  - 权限：todos:read/write/delete，projects:read/write/delete，tasks:read/write/delete

你可以通过环境变量覆盖默认用户名和密码：
  ADMIN_USERNAME / ADMIN_PASSWORD
  NORMAL_USERNAME / NORMAL_PASSWORD

使用方式：

    cd rbac_auth_service
    python init_rbac_data.py
"""

from __future__ import annotations

import os

from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine
from app import models, security


def get_env(key: str, default: str) -> str:
    """读取环境变量，若不存在则使用默认值。"""
    return os.getenv(key, default)


def init_data(db: Session) -> None:
    """初始化基础 RBAC 数据（幂等）。"""
    # 创建权限
    perm_codes = [
        ("todos:read", "读取 TODO"),
        ("todos:write", "创建/更新 TODO"),
        ("todos:delete", "删除 TODO"),
        ("projects:read", "读取项目"),
        ("projects:write", "创建/更新项目"),
        ("projects:delete", "删除项目"),
        ("tasks:read", "读取任务"),
        ("tasks:write", "创建/更新任务"),
        ("tasks:delete", "删除任务"),
    ]
    perms_by_code: dict[str, models.Permission] = {}
    for code, name in perm_codes:
        perm = (
            db.query(models.Permission)
            .filter(models.Permission.code == code)
            .first()
        )
        if not perm:
            perm = models.Permission(code=code, name=name)
            db.add(perm)
        perms_by_code[code] = perm

    # 创建角色
    role_admin = (
        db.query(models.Role).filter(models.Role.name == "admin").first()
    )
    if not role_admin:
        role_admin = models.Role(name="admin", description="管理员")
        db.add(role_admin)

    role_user = (
        db.query(models.Role).filter(models.Role.name == "user").first()
    )
    if not role_user:
        role_user = models.Role(name="user", description="普通用户")
        db.add(role_user)

    db.flush()

    # 分配权限给角色
    role_admin.permissions = list(perms_by_code.values())
    role_user.permissions = [
        perms_by_code["todos:read"],
        perms_by_code["todos:write"],
        perms_by_code["projects:read"],
        perms_by_code["projects:write"],
        perms_by_code["tasks:read"],
        perms_by_code["tasks:write"],
    ]

    # 创建用户
    admin_username = get_env("ADMIN_USERNAME", "admin")
    admin_password = get_env("ADMIN_PASSWORD", "admin123")
    normal_username = get_env("NORMAL_USERNAME", "alice")
    normal_password = get_env("NORMAL_PASSWORD", "alice123")

    admin = (
        db.query(models.User)
        .filter(models.User.username == admin_username)
        .first()
    )
    if not admin:
        admin = models.User(
            username=admin_username,
            hashed_password=security.hash_password(admin_password),
            is_superuser=True,
        )
        db.add(admin)

    normal = (
        db.query(models.User)
        .filter(models.User.username == normal_username)
        .first()
    )
    if not normal:
        normal = models.User(
            username=normal_username,
            hashed_password=security.hash_password(normal_password),
        )
        db.add(normal)

    db.flush()

    # 为普通用户分配 user 角色
    if role_user not in normal.roles:
        normal.roles.append(role_user)

    db.commit()

    print("✅ RBAC 基础数据初始化完成：")
    print(f"  超管：{admin_username} / {admin_password}")
    print(f"  普通用户：{normal_username} / {normal_password}")
    print("  角色：admin, user")
    print(
        "  权限：todos:read, todos:write, todos:delete, "
        "projects:read, projects:write, projects:delete, "
        "tasks:read, tasks:write, tasks:delete"
    )


def main() -> None:
    """脚本主入口。"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        init_data(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
