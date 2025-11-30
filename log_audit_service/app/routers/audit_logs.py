"""
审计日志相关 API 路由。
"""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..repositories.audit_log_repository import create_audit_log, query_audit_logs
from ..schemas import AuditLogCreate, AuditLogRead


router = APIRouter(prefix="/logs", tags=["audit_logs"])


@router.post("", response_model=AuditLogRead, status_code=201)
def create_log(log_in: AuditLogCreate, db: Session = Depends(get_db)) -> AuditLogRead:
    """
    创建一条审计日志。

    通常由其他服务在关键操作（如登录、下单、权限变更等）完成后调用。
    """
    log = create_audit_log(db, log_in)
    return log


@router.get("", response_model=List[AuditLogRead])
def list_logs(
    actor: Optional[str] = Query(None, description="按 actor 精确过滤"),
    action: Optional[str] = Query(None, description="按 action 精确过滤"),
    source_service: Optional[str] = Query(
        None, description="按来源服务名称精确过滤"
    ),
    since: Optional[datetime] = Query(
        None, description="起始时间（含），ISO8601 格式"
    ),
    until: Optional[datetime] = Query(
        None, description="结束时间（含），ISO8601 格式"
    ),
    limit: int = Query(50, ge=1, le=200, description="返回记录数量上限"),
    offset: int = Query(0, ge=0, description="偏移量，用于分页"),
    db: Session = Depends(get_db),
) -> List[AuditLogRead]:
    """
    按条件查询审计日志列表。

    支持按 actor/action/source_service 以及时间范围过滤，默认按时间倒序返回。
    """
    logs = query_audit_logs(
        db,
        actor=actor,
        action=action,
        source_service=source_service,
        since=since,
        until=until,
        limit=limit,
        offset=offset,
    )
    return list(logs)


@router.get("/ui", response_class=HTMLResponse)
def logs_ui(
    request: Request,
    actor: Optional[str] = Query(None, description="按 actor 精确过滤"),
    action: Optional[str] = Query(None, description="按 action 精确过滤"),
    source_service: Optional[str] = Query(
        None, description="按来源服务名称精确过滤"
    ),
    limit: int = Query(50, ge=1, le=200, description="返回记录数量上限"),
    db: Session = Depends(get_db),
) -> HTMLResponse:
    """
    简单的 HTML 审计日志查看界面。

    仅用于本地开发与学习，便于在浏览器中快速查看最近的审计日志。
    """
    logs = query_audit_logs(
        db,
        actor=actor,
        action=action,
        source_service=source_service,
        since=None,
        until=None,
        limit=limit,
        offset=0,
    )

    def esc(value: Optional[str]) -> str:
        if value is None:
            return ""
        return (
            str(value)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

    rows = []
    for log in logs:
        rows.append(
            f"<tr>"
            f"<td>{log.id}</td>"
            f"<td>{esc(log.actor)}</td>"
            f"<td>{esc(log.action)}</td>"
            f"<td>{esc(log.resource)}</td>"
            f"<td>{esc(log.source_service)}</td>"
            f"<td>{log.created_at}</td>"
            f"<td>{esc(log.ip)}</td>"
            f"<td>{esc(log.detail)}</td>"
            f"</tr>"
        )
    rows_html = "\n".join(rows)

    html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <title>审计日志查看</title>
  <style>
    body {{ font-family: sans-serif; padding: 16px; }}
    table {{ border-collapse: collapse; width: 100%; margin-top: 12px; }}
    th, td {{ border: 1px solid #ddd; padding: 4px 8px; font-size: 13px; }}
    th {{ background: #f5f5f5; }}
    form > * {{ margin-right: 8px; }}
  </style>
  </head>
  <body>
    <h1>审计日志查看</h1>
    <form method="get" action="{request.url.path}">
      <label>Actor:
        <input type="text" name="actor" value="{esc(actor) if actor else ''}" />
      </label>
      <label>Action:
        <input type="text" name="action" value="{esc(action) if action else ''}" />
      </label>
      <label>Source Service:
        <input type="text" name="source_service" value="{esc(source_service) if source_service else ''}" />
      </label>
      <label>Limit:
        <input type="number" name="limit" min="1" max="200" value="{limit}" />
      </label>
      <button type="submit">筛选</button>
    </form>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Actor</th>
          <th>Action</th>
          <th>Resource</th>
          <th>Source</th>
          <th>Created At</th>
          <th>IP</th>
          <th>Detail</th>
        </tr>
      </thead>
      <tbody>
        {rows_html}
      </tbody>
    </table>
  </body>
</html>
    """
    return HTMLResponse(content=html)
