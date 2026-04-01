"""
日志侦探服务配置。

职责：
- 给 analyzer.py 提供日志大小、行数、正则长度、结果条数等限制；
- 让接口层和分析层共享同一组边界条件。
"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """日志侦探服务配置类。"""

    SERVICE_NAME: str = "log_detective_service"
    SERVICE_PORT: int = 8084
    # 单次请求允许提交的最大原始日志文本大小。
    MAX_LOG_SIZE: int = 2_000_000  # 2MB
    # 进入分析前最多保留多少行，避免超大日志把分析时间和内存拖爆。
    MAX_LOG_LINES: int = 50_000
    # 正则分析允许的最大耗时，超时后会按 regex_timeout=True 返回 meta 信息。
    REGEX_TIMEOUT: int = 2  # 秒
    # 自定义正则最长长度，避免教学场景里传入过长表达式。
    MAX_REGEX_LENGTH: int = 500
    # suspicious_ips / critical_errors 等结果集合的统一上限。
    MAX_RESULTS: int = 1000

# 模块级单例：整个服务共享同一份限制配置。
settings = Settings()
