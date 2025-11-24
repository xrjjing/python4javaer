import argparse
from collections import Counter
from pathlib import Path


def analyze_log(path: Path) -> Counter[str]:
    """
    分析日志文件，按日志级别统计数量。

    默认假设每行日志格式类似：
    2025-01-01 12:00:00 [INFO] something happened...
    """
    if not path.is_file():
        raise ValueError(f"日志文件不存在：{path}")

    level_counter: Counter[str] = Counter()

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if "[" in line and "]" in line:
                # 简单解析出中括号中的日志级别
                level = line.split("[", 1)[1].split("]", 1)[0]
                level_counter[level] += 1

    return level_counter


def parse_args() -> argparse.Namespace:
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(description="简单日志分析工具")
    parser.add_argument("log_file", help="日志文件路径")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    log_path = Path(args.log_file)
    level_counter = analyze_log(log_path)

    print("按日志级别统计结果：")
    for level, count in level_counter.most_common():
        print(f"{level}: {count}")


if __name__ == "__main__":
    main()

