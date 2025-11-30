"""
审计日志数据访问层。
"""

from datetime import datetime
from typing import Iterable, Optional

from sqlalchemy.orm import Session

from ..models import AuditLog
from ..schemas import AuditLogCreate


def create_audit_log(db: Session, log_in: AuditLogCreate) -> AuditLog:
    """创建一条审计日志记录。"""
    log = AuditLog(
        actor=log_in.actor,
        action=log_in.action,
        resource=log_in.resource,
        source_service=log_in.source_service,
        ip=log_in.ip,
        detail=log_in.detail,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def query_audit_logs(
    db: Session,
    *,
    actor: Optional[str] = None,
    action: Optional[str] = None,
    source_service: Optional[str] = None,
    since: Optional[datetime] = None,
    until: Optional[datetime] = None,
    limit: int = 50,
    offset: int = 0,
) -> Iterable[AuditLog]:
    """按条件查询审计日志列表。"""
    query = db.query(AuditLog)

    if actor:
        query = query.filter(AuditLog.actor == actor)
    if action:
        query = query.filter(AuditLog.action == action)
    if source_service:
        query = query.filter(AuditLog.source_service == source_service)
    if since:
        query = query.filter(AuditLog.created_at >= since)
    if until:
        query = query.filter(AuditLog.created_at <= until)

    query = query.order_by(AuditLog.created_at.desc())
    return query.offset(offset).limit(limit).all()

