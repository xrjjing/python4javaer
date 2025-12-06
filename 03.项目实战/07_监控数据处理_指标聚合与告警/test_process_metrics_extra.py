from pathlib import Path

from process_metrics import aggregate_metrics, check_thresholds, load_metrics


def test_aggregate_metrics_average(tmp_path: Path, capsys):
    csv_path = tmp_path / "metrics.csv"
    csv_path.write_text(
        "metric,value\nhttp_requests_duration_ms,100\nhttp_requests_duration_ms,400\n",
        encoding="utf-8",
    )

    rows = load_metrics(csv_path)
    stats = aggregate_metrics(rows)
    assert stats["http_requests_duration_ms"].count == 2
    assert stats["http_requests_duration_ms"].average == 250

    check_thresholds(stats)
    out = capsys.readouterr().out
    assert "超出阈值" in out
