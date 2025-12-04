from pydantic import BaseModel, Field
from typing import Optional, Literal, List
from datetime import datetime
from .config import settings


class LogDetectiveRequest(BaseModel):
    log_text: str = Field(..., min_length=1, max_length=settings.MAX_LOG_SIZE, description="日志文本内容")
    profile: Literal["nginx_access", "nginx_error", "python_app", "generic"] = Field(
        default="generic", description="预定义解析模式"
    )
    custom_regex: Optional[str] = Field(None, max_length=settings.MAX_REGEX_LENGTH, description="自定义正则(教学用)")
    max_results: int = Field(default=settings.MAX_RESULTS, gt=0, le=settings.MAX_RESULTS, description="最大结果数")


class IpStat(BaseModel):
    ip: str
    count: int
    first_seen: Optional[str] = None
    last_seen: Optional[str] = None
    reason: str = ""


class ErrorRecord(BaseModel):
    timestamp: Optional[str] = None
    level: str
    message: str
    line_no: int


class LogAnalysisSummary(BaseModel):
    total_lines: int
    error_lines: int
    warn_lines: int
    time_range: Optional[str] = None


class LogAnalysisResult(BaseModel):
    summary: LogAnalysisSummary
    suspicious_ips: List[IpStat] = Field(default_factory=list)
    critical_errors: List[ErrorRecord] = Field(default_factory=list)
    meta: dict = Field(default_factory=dict)
