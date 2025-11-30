"""
日志 / 审计服务数据库模型定义。
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


Index("idx_audit_logs_actor_created_at", AuditLog.actor, AuditLog.created_at)
Index("idx_audit_logs_action_created_at", AuditLog.action, AuditLog.created_at)

