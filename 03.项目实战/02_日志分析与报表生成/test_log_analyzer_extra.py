from pathlib import Path

from log_analyzer import analyze_log


def test_analyze_log_counts(tmp_path: Path):
    log_file = tmp_path / "app.log"
    log_file.write_text(
        """\
2025-01-01 00:00:00 [INFO] ok
2025-01-01 00:00:01 [ERROR] bad
2025-01-01 00:00:02 [INFO] ok
""",
        encoding="utf-8",
    )

    counter = analyze_log(log_file)
    assert counter["INFO"] == 2
    assert counter["ERROR"] == 1
