import re
import signal
from typing import Optional, List, Dict
from collections import defaultdict
from multiprocessing import Process, Queue
from .schemas import LogDetectiveRequest, LogAnalysisResult, LogAnalysisSummary, IpStat, ErrorRecord
from .config import settings


class TimeoutException(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutException()


PATTERNS = {
    "nginx_access": r'(\d+\.\d+\.\d+\.\d+).*?"[^"]*"\s+(\d{3})',
    "nginx_error": r'(\d{4}/\d{2}/\d{2}\s+\d{2}:\d{2}:\d{2})\s+\[(\w+)\]\s+(.*)',
    "python_app": r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}).*?\[(\w+)\]\s+(.*)',
    "generic": r'(ERROR|WARN|INFO|CRITICAL|DEBUG)',
}


def _safe_regex_match(pattern: str, text: str, timeout: int, result_queue: Queue):
    """子进程中执行正则匹配"""
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
    """带超时保护的正则匹配"""
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


def analyze_logs(request: LogDetectiveRequest) -> LogAnalysisResult:
    """分析日志(不记录原始内容,仅内存处理)"""
    all_lines = request.log_text.split('\n')
    lines = all_lines[:settings.MAX_LOG_LINES]
    truncated = len(request.log_text) >= settings.MAX_LOG_SIZE or len(all_lines) > settings.MAX_LOG_LINES

    # 基础统计
    total_lines = len(lines)
    error_lines = sum(1 for line in lines if 'ERROR' in line.upper())
    warn_lines = sum(1 for line in lines if 'WARN' in line.upper())

    # IP统计
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    ip_counts: Dict[str, int] = defaultdict(int)

    for line in lines:
        ips = re.findall(ip_pattern, line)
        for ip in ips:
            if 'ERROR' in line.upper() or 'WARN' in line.upper():
                ip_counts[ip] += 1

    suspicious_ips = [
        IpStat(ip=ip, count=count, reason="多次错误/警告")
        for ip, count in sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    ]

    # 关键错误
    critical_errors = []
    for i, line in enumerate(lines[:100]):  # 只取前100行关键错误
        if 'ERROR' in line.upper() or 'CRITICAL' in line.upper():
            critical_errors.append(ErrorRecord(
                level="ERROR" if 'ERROR' in line.upper() else "CRITICAL",
                message=line[:200],  # 限制长度
                line_no=i + 1
            ))

    return LogAnalysisResult(
        summary=LogAnalysisSummary(
            total_lines=total_lines,
            error_lines=error_lines,
            warn_lines=warn_lines
        ),
        suspicious_ips=suspicious_ips,
        critical_errors=critical_errors[:request.max_results],
        meta={"truncated": truncated}
    )
