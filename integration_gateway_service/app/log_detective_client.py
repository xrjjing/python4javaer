"""
日志侦探服务客户端封装。

该模块负责与日志侦探服务进行通信，提供日志分析功能的调用接口。
"""

from typing import Any, Dict

import httpx

from .config import settings


class LogDetectiveServiceError(Exception):
    """表示调用日志侦探服务过程中发生的异常。"""


class LogDetectiveClient:
    """日志侦探服务客户端封装。"""

    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = base_url or str(settings.log_detective_base_url)

    async def analyze_logs(self, log_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        调用日志侦探服务分析日志。

        Args:
            log_request: 日志分析请求体，包含 log_text、profile、max_results 等字段

        Returns:
            分析结果字典，包含 summary、suspicious_ips、critical_errors 等

        Raises:
            LogDetectiveServiceError: 调用服务失败时抛出
        """
        url = f"{self.base_url}/internal/log-detective/analyze"

        try:
            async with httpx.AsyncClient(timeout=30.0, trust_env=False) as client:
                resp = await client.post(url, json=log_request)
                resp.raise_for_status()
                return resp.json()
        except httpx.TimeoutException as exc:
            raise LogDetectiveServiceError("日志分析服务超时") from exc
        except httpx.HTTPStatusError as exc:
            raise LogDetectiveServiceError(
                f"日志分析服务返回错误，状态码：{exc.response.status_code}"
            ) from exc
        except httpx.HTTPError as exc:
            raise LogDetectiveServiceError(
                f"调用日志分析服务失败：{str(exc)}"
            ) from exc
        except ValueError as exc:
            raise LogDetectiveServiceError(
                "日志分析服务返回了非 JSON 格式的数据"
            ) from exc
