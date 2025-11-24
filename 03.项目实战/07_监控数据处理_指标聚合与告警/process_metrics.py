import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List


@dataclass
class MetricStat:
    count: int = 0
    total: float = 0.0
    max_value: float = float("-inf")

    def add(self, value: float) -> None:
        self.count += 1
        self.total += value
        if value > self.max_value:
            self.max_value = value

    @property
    def average(self) -> float:
        if self.count == 0:
            return 0.0
        return self.total / self.count


def load_metrics(path: Path) -> List[Dict[str, str]]:
    """从 CSV 文件加载监控数据。"""
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def aggregate_metrics(rows: List[Dict[str, str]]) -> Dict[str, MetricStat]:
    """按指标名称聚合统计。"""
    stats: Dict[str, MetricStat] = defaultdict(MetricStat)
    for row in rows:
        name = row["metric"]
        value = float(row["value"])
        stats[name].add(value)
    return stats


def check_thresholds(stats: Dict[str, MetricStat]) -> None:
    """
    简单阈值检查。

    为了演示，这里直接在代码中写死一些指标的阈值规则：
    - http_requests_duration_ms: max > 300 视为告警
    """
    if "http_requests_duration_ms" in stats:
        s = stats["http_requests_duration_ms"]
        if s.max_value > 300:
            print(
                "[告警] http_requests_duration_ms 最大值超出阈值：",
                s.max_value,
            )


def main() -> None:
    data_path = Path(
        "03.项目实战/07_监控数据处理_指标聚合与告警/metrics_sample.csv"
    )
    if not data_path.is_file():
        print(f"请先在该目录下准备示例数据文件：{data_path}")
        return

    rows = load_metrics(data_path)
    stats = aggregate_metrics(rows)

    print("=== 指标统计结果 ===")
    for name, s in stats.items():
        print(
            f"{name}: count={s.count}, avg={s.average:.2f}, max={s.max_value:.2f}"
        )

    print("\n=== 阈值检查 ===")
    check_thresholds(stats)


if __name__ == "__main__":
    main()

