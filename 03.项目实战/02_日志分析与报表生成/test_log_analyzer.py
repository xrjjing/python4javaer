"""log_analyzer 日志分析脚本的基础单元测试。"""

from pathlib import Path

import sys


def _import_log_analyzer():
    """动态导入 log_analyzer 模块。"""
    current_dir = Path(__file__).resolve().parent
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))
    import log_analyzer  # type: ignore

    return log_analyzer


def test_analyze_log_counts_levels(tmp_path: Path) -> None:
    """给定简单日志内容时，应按级别正确统计数量。"""
    log_analyzer = _import_log_analyzer()

    content = "\n".join(
        [
            "2025-01-01 00:00:00 [INFO] start",
            "2025-01-01 00:00:01 [WARN] warn1",
            "2025-01-01 00:00:02 [ERROR] err1",
            "2025-01-01 00:00:03 [ERROR] err2",
        ]
    )
    log_file = tmp_path / "sample.log"
    log_file.write_text(content, encoding="utf-8")

    counter = log_analyzer.analyze_log(log_file)

    assert counter["INFO"] == 1
    assert counter["WARN"] == 1
    assert counter["ERROR"] == 2


def test_analyze_log_invalid_path(tmp_path: Path) -> None:
    """日志路径不存在时，应抛出 ValueError。"""
    log_analyzer = _import_log_analyzer()
    missing = tmp_path / "missing.log"

    try:
        log_analyzer.analyze_log(missing)
    except ValueError as exc:
        assert "日志文件不存在" in str(exc)
    else:
        raise AssertionError("预期应抛出 ValueError")

