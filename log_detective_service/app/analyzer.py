"""
日志侦探核心分析模块。

这里是整个服务最重要的业务核心，负责：
- 选择预定义正则或自定义正则；
- 对正则执行增加超时保护；
- 统计错误 / 警告；
- 提取可疑 IP；
- 识别关键错误记录。

排查建议：
- 返回 400：先看 custom_regex / 长度限制；
- 返回结果为空或数量异常：继续看这里的过滤与截断逻辑。
"""

import re
import signal
from typing import Optional, List, Dict, Any
from collections import defaultdict
from multiprocessing import Process, Queue
from .schemas import LogDetectiveRequest, LogAnalysisResult, LogAnalysisSummary, IpStat, ErrorRecord
from .config import settings


class TimeoutException(Exception):
    """正则子进程超时异常。"""
    pass


def timeout_handler(signum, frame):
    """signal alarm 的处理函数，用于中断耗时过长的正则。"""
    raise TimeoutException()


# 预定义日志模式：profile 字段最终会映射到这里的正则。
PATTERNS: Dict[str, str] = {
    "nginx_access": r'(\d+\.\d+\.\d+\.\d+).*?"[^"]*"\s+(\d{3})',
    "nginx_error": r'(\d{4}/\d{2}/\d{2}\s+\d{2}:\d{2}:\d{2})\s+\[(\w+)\]\s+(.*)',
    "python_app": r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}).*?\[(\w+)\]\s+(.*)',
    "generic": r'(ERROR|WARN|INFO|CRITICAL|DEBUG)',
}


def _safe_regex_match(pattern: str, text: str, timeout: int, result_queue: Queue):
    """子进程中执行正则匹配。"""
    try:
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout)

        compiled = re.compile(pattern)
        matches = compiled.findall(text)

        signal.alarm(0)
        result_queue.put(("success", matches))
    except TimeoutException:
        result_queue.put(("timeout", None))
    except Exception as e:
        result_queue.put(("error", str(e)))


def safe_regex_match(pattern: str, text: str, timeout: int = 2) -> Optional[List]:
    """
    带超时保护的正则匹配。

    这里单独起子进程，是为了尽量避免复杂正则把主服务线程卡住。
    """
    result_queue = Queue()
    process = Process(target=_safe_regex_match, args=(pattern, text, timeout, result_queue))

    process.start()
    process.join(timeout + 1)

    if process.is_alive():
        process.terminate()
        process.join()
        return None

    if not result_queue.empty():
        status, result = result_queue.get()
        if status == "success":
            return result

    return None


# 日志分析主入口：router 层只做请求接收，真正的统计和提取都在这里。
def analyze_logs(request: LogDetectiveRequest) -> LogAnalysisResult:
    """
    分析日志（不记录原始内容，仅内存处理）。

    这是 router 层真正调用的业务入口。
    """
    all_lines = request.log_text.split("\n")
    lines = all_lines[: settings.MAX_LOG_LINES]
    truncated = len(request.log_text) >= settings.MAX_LOG_SIZE or len(all_lines) > settings.MAX_LOG_LINES

    # ===== 正则匹配入口：先根据 profile / custom_regex 决定要用哪条规则 =====
    if request.custom_regex and len(request.custom_regex) > settings.MAX_REGEX_LENGTH:
        raise ValueError("自定义正则长度超过限制")

    pattern = request.custom_regex or PATTERNS.get(request.profile, PATTERNS["generic"])
    regex_matches: Optional[List[Any]] = safe_regex_match(pattern, "\n".join(lines), timeout=settings.REGEX_TIMEOUT)

    # ===== 基础统计：这些数字会直接回到前端统计卡片区 =====
    total_lines = len(lines)
    error_lines = sum(1 for line in lines if "ERROR" in line.upper())
    warn_lines = sum(1 for line in lines if "WARN" in line.upper())

    # ===== IP 统计：默认按 ERROR / WARN 行里的 IP 加权，nginx_access 再额外按 4xx/5xx 叠加 =====
    ip_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
    ip_counts: Dict[str, int] = defaultdict(int)

    for line in lines:
        ips = re.findall(ip_pattern, line)
        for ip in ips:
            if "ERROR" in line.upper() or "WARN" in line.upper():
                ip_counts[ip] += 1

    # 如果是 nginx_access, 用匹配结果按 4xx/5xx 加权统计
    if request.profile == "nginx_access" and regex_matches:
        for ip, status in regex_matches:
            try:
                status_int = int(status)
                if status_int >= 400:
                    ip_counts[ip] += 1
            except Exception:
                continue

    suspicious_ips = [
        IpStat(ip=ip, count=count, reason="多次错误/警告")
        for ip, count in sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    ]

    # ===== 关键错误提取：优先用结构化结果，否则退回文本扫描 =====
    critical_errors: List[ErrorRecord] = []
    # 如果 profile 为 python_app 且正则解析成功，使用结构化结果
    if request.profile == "python_app" and regex_matches:
        for ts, level, msg in regex_matches[: request.max_results]:
            level_upper = str(level).upper()
            if level_upper in ("ERROR", "CRITICAL"):
                critical_errors.append(
                    ErrorRecord(
                        timestamp=str(ts),
                        level=level_upper,
                        message=str(msg)[:200],
                        line_no=0,
                    )
                )
    else:
        # 回退：基于文本扫描前 100 行
        for i, line in enumerate(lines[:100]):
            if "ERROR" in line.upper() or "CRITICAL" in line.upper():
                critical_errors.append(
                    ErrorRecord(
                        level="ERROR" if "ERROR" in line.upper() else "CRITICAL",
                        message=line[:200],
                        line_no=i + 1,
                    )
                )

    # meta 主要给调用方解释“这次分析到底是怎么跑出来的”。
    meta = {
        "truncated": truncated,
        "regex_used": "custom" if request.custom_regex else request.profile,
        "regex_timeout": regex_matches is None,
        "regex_matches": 0 if regex_matches is None else len(regex_matches),
    }

    return LogAnalysisResult(
        summary=LogAnalysisSummary(
            total_lines=total_lines,
            error_lines=error_lines,
            warn_lines=warn_lines,
        ),
        suspicious_ips=suspicious_ips,
        critical_errors=critical_errors[: request.max_results],
        meta=meta,
    )
