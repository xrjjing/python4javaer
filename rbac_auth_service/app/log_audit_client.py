"""
日志 / 审计服务客户端封装。

该模块提供一个简单的审计日志上报工具，用于在 RBAC 服务的关键操作
（如登录、登出等）完成后，将行为投递到独立的 log_audit_service。

设计原则：
- 若未配置 log_audit_base_url，则静默忽略，不影响主流程；
- 调用失败时捕获异常并忽略，避免因为日志服务不可用影响业务。
"""

from typing import Any, Dict

import httpx

from .config import settings


class LogAuditClient:
    """审计日志客户端。"""

    def __init__(self, base_url: str | None = None) -> None:
        self._base_url = base_url

    @property
    def base_url(self) -> str | None:
        """返回当前使用的日志服务基础地址。"""
        return self._base_url or (str(settings.log_audit_base_url) if settings.log_audit_base_url else None)

    def send_log(self, payload: Dict[str, Any]) -> None:
        """
        发送审计日志到日志服务。

        若未配置地址或请求失败，将静默忽略，不抛出异常。
        """
        base = self.base_url
        if not base:
            return

        url = f"{base.rstrip('/')}/logs"
        try:
            httpx.post(url, json=payload, timeout=2.0)
        except Exception:
            # 日志上报失败不影响主流程
            return


log_audit_client = LogAuditClient()

