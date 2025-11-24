"""process_metrics 指标聚合与告警脚本的基础单元测试。"""

from pathlib import Path

import sys


def _import_metrics():
    """动态导入 process_metrics 模块。"""
    current_dir = Path(__file__).resolve().parent
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))
    import process_metrics  # type: ignore

    return process_metrics


def test_aggregate_metrics_and_average(tmp_path: Path) -> None:
    """应能按指标名称正确聚合 count / avg / max。"""
    metrics = _import_metrics()

    rows = [
        {"metric": "http_requests_duration_ms", "value": "100"},
        {"metric": "http_requests_duration_ms", "value": "300"},
        {"metric": "cpu_usage", "value": "50"},
    ]

    stats = metrics.aggregate_metrics(rows)

    http_stat = stats["http_requests_duration_ms"]
    assert http_stat.count == 2
    assert http_stat.max_value == 300
    assert http_stat.average == 200

    cpu_stat = stats["cpu_usage"]
    assert cpu_stat.count == 1
    assert cpu_stat.max_value == 50

