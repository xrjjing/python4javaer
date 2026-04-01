"""
日志侦探服务的请求 / 响应模型。

这些模型同时承担三层职责：
- 约束前端 / 网关发来的请求体；
- 限制分析参数范围；
- 规定前端结果区能拿到哪些字段。
"""

from pydantic import BaseModel, Field
from typing import Optional, Literal, List
from datetime import datetime
from .config import settings


class LogDetectiveRequest(BaseModel):
    """日志分析请求体。"""

    # 前端 textarea / 网关请求体最终都会落到这个字段。
    log_text: str = Field(..., min_length=1, max_length=settings.MAX_LOG_SIZE, description="日志文本内容")
    # profile 用于选择 analyzer.py 里的预定义 PATTERNS。
    profile: Literal["nginx_access", "nginx_error", "python_app", "generic"] = Field(
        default="generic", description="预定义解析模式"
    )
    # 教学用途的可选自定义正则；若传入则优先级高于 profile。
    custom_regex: Optional[str] = Field(None, max_length=settings.MAX_REGEX_LENGTH, description="自定义正则(教学用)")
    max_results: int = Field(default=settings.MAX_RESULTS, gt=0, le=settings.MAX_RESULTS, description="最大结果数")


class IpStat(BaseModel):
    """可疑 IP 统计项。"""

    ip: str
    count: int
    first_seen: Optional[str] = None
    last_seen: Optional[str] = None
    reason: str = ""


class ErrorRecord(BaseModel):
    """关键错误记录。"""

    timestamp: Optional[str] = None
    level: str
    message: str
    line_no: int


class LogAnalysisSummary(BaseModel):
    """汇总统计信息。"""

    total_lines: int
    error_lines: int
    warn_lines: int
    time_range: Optional[str] = None


class LogAnalysisResult(BaseModel):
    """完整分析结果，前端结果区最终就是围绕这个结构渲染。"""

    # 顶部统计卡片区使用 summary。
    summary: LogAnalysisSummary
    # “可疑 IP” 表格区使用 suspicious_ips。
    suspicious_ips: List[IpStat] = Field(default_factory=list)
    # “关键错误” 表格区使用 critical_errors。
    critical_errors: List[ErrorRecord] = Field(default_factory=list)
    # meta 主要给调用方说明这次分析是否截断、超时、用了哪条规则。
    meta: dict = Field(default_factory=dict)
