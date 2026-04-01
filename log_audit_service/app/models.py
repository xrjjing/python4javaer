"""
日志 / 审计服务数据库模型定义。

当前只有一个核心表：audit_logs。
admin.html 查看日志、本地 /ui 页面查看日志，最终都依赖这张表。
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text, Index

from .database import Base


class AuditLog(Base):
    """审计日志模型。"""

    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    actor = Column(String(100), nullable=True, index=True)
    action = Column(String(100), nullable=False, index=True)
    resource = Column(String(100), nullable=True, index=True)
    source_service = Column(String(100), nullable=True, index=True)
    ip = Column(String(45), nullable=True)
    detail = Column(Text, nullable=True)


# 组合索引：便于按 actor / action + 时间倒序过滤最近日志。
Index("idx_audit_logs_actor_created_at", AuditLog.actor, AuditLog.created_at)
Index("idx_audit_logs_action_created_at", AuditLog.action, AuditLog.created_at)
