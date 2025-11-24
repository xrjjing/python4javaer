import argparse
import datetime as dt
from pathlib import Path
from typing import Iterable
from zipfile import ZIP_DEFLATED, ZipFile


def find_old_logs(
    directory: Path, days: int, exts: Iterable[str]
) -> list[Path]:
    """查找指定目录下超过 N 天的日志文件。"""
    cutoff = dt.datetime.now() - dt.timedelta(days=days)
    exts = {("." + e.lower().lstrip(".")) for e in exts}
    result: list[Path] = []

    for path in directory.iterdir():
        if not path.is_file():
            continue
        if exts and path.suffix.lower() not in exts:
            continue

        mtime = dt.datetime.fromtimestamp(path.stat().st_mtime)
        if mtime < cutoff:
            result.append(path)
    return result


def archive_files(files: list[Path], archive_path: Path) -> None:
    """将文件压缩到 zip 包中。"""
    with ZipFile(archive_path, "w", compression=ZIP_DEFLATED) as zf:
        for f in files:
            # 将文件名写入 zip，避免包含完整路径
            zf.write(f, arcname=f.name)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="归档超过 N 天的日志文件")
    parser.add_argument("--dir", default="./logs", help="日志目录，默认 ./logs")
    parser.add_argument("--days", type=int, default=7, help="阈值天数，默认 7 天")
    parser.add_argument(
        "--ext",
        default="log",
        help="需要处理的扩展名，逗号分隔，默认 log，如 log,out",
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="归档成功后删除原始日志文件",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    directory = Path(args.dir)
    if not directory.is_dir():
        raise ValueError(f"日志目录不存在：{directory}")

    exts = [e.strip() for e in args.ext.split(",") if e.strip()]
    files = find_old_logs(directory, days=args.days, exts=exts)

    if not files:
        print("没有需要归档的日志文件。")
        return

    archive_name = f"{directory.name}_archive_{dt.date.today().isoformat()}.zip"
    archive_path = directory.parent / archive_name

    print("将归档以下文件：")
    for f in files:
        print("-", f)

    archive_files(files, archive_path)
    print(f"已生成归档文件：{archive_path.resolve()}")

    if args.delete:
        for f in files:
            f.unlink()
        print("已删除原始日志文件。")


if __name__ == "__main__":
    main()

