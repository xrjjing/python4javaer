import argparse
from pathlib import Path


def rename_files(
    directory: Path,
    prefix: str | None = None,
    suffix: str | None = None,
    dry_run: bool = False,
    extensions: list[str] | None = None,
) -> None:
    """
    批量重命名目录中的文件。

    :param directory: 目标目录路径
    :param prefix: 文件名前缀（可选）
    :param suffix: 文件名后缀（可选）
    :param dry_run: 是否仅打印不实际重命名
    :param extensions: 只处理这些扩展名（不带点，如 ["jpg", "png"]），None 表示不过滤
    """
    if not directory.is_dir():
        raise ValueError(f"目录不存在：{directory}")

    # 统一扩展名为小写，便于对比
    if extensions is not None:
        extensions = [ext.lower() for ext in extensions]

    files = sorted(p for p in directory.iterdir() if p.is_file())
    for index, path in enumerate(files, start=1):
        if extensions is not None:
            if path.suffix:
                ext = path.suffix.lstrip(".").lower()
                if ext not in extensions:
                    continue

        stem = path.stem
        new_stem = stem
        if prefix:
            new_stem = prefix + new_stem
        if suffix:
            new_stem = new_stem + suffix

        new_name = f"{index:03d}_{new_stem}{path.suffix}"
        new_path = path.with_name(new_name)

        if dry_run:
            print(f"[预览] {path.name} -> {new_path.name}")
        else:
            print(f"[重命名] {path.name} -> {new_path.name}")
            path.rename(new_path)


def parse_args() -> argparse.Namespace:
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(description="批量重命名目录中的文件")
    parser.add_argument("directory", help="目标目录路径")
    parser.add_argument("--prefix", help="文件名前缀", default="")
    parser.add_argument("--suffix", help="文件名后缀", default="")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="预览模式，仅打印结果而不实际重命名",
    )
    parser.add_argument(
        "--ext",
        help="只处理这些扩展名（用逗号分隔，不带点，如 jpg,png）",
        default="",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    directory = Path(args.directory)
    extensions = (
        [ext.strip() for ext in args.ext.split(",") if ext.strip()] if args.ext else None
    )
    rename_files(
        directory,
        prefix=args.prefix or None,
        suffix=args.suffix or None,
        dry_run=bool(args.dry_run),
        extensions=extensions,
    )


if __name__ == "__main__":
    main()

