"""
文件与目录操作深入示例

本模块演示以下常见场景：
1. 使用 pathlib 表示路径与遍历目录；
2. 使用 rglob / glob 进行文件过滤；
3. 使用 shutil 复制/移动/删除目录树；
4. 使用 tempfile 处理临时目录；
5. 一个简单的「日志归档」脚本雏形。

注意：为安全起见，这里的示例尽量避免真正删除你项目中的文件，
可以在一个单独的测试目录中运行练习代码。
"""

from __future__ import annotations

import shutil
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterable, List


def find_files_by_suffix(root: Path, suffix: str) -> list[Path]:
    """
    递归查找指定后缀的所有文件。

    :param root: 起始目录
    :param suffix: 后缀名，例如 '.log'、'.txt'
    :return: 所有匹配的文件路径列表
    """
    if not root.is_dir():
        raise ValueError(f"目录不存在：{root}")
    return [p for p in root.rglob(f"*{suffix}") if p.is_file()]


def copy_tree(src: Path, dst: Path) -> None:
    """
    复制整个目录树到目标位置。

    如果目标已存在，允许覆盖（dirs_exist_ok=True）。
    """
    if not src.is_dir():
        raise ValueError(f"源目录不存在：{src}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dst, dirs_exist_ok=True)


def move_old_logs(
    log_dir: Path,
    archive_dir: Path,
    days: int = 7,
    dry_run: bool = True,
) -> list[tuple[Path, Path]]:
    """
    将 log_dir 中「最后修改时间早于 N 天之前」的日志文件移动到 archive_dir。

    :param log_dir: 日志目录
    :param archive_dir: 归档目录
    :param days: 阈值天数（早于该天数的视为旧日志）
    :param dry_run: 是否只打印计划的移动操作，而不真正执行
    :return: (源路径, 目标路径) 列表，方便调试或测试
    """
    if not log_dir.is_dir():
        raise ValueError(f"日志目录不存在：{log_dir}")

    archive_dir.mkdir(parents=True, exist_ok=True)

    threshold = datetime.now() - timedelta(days=days)
    planned_moves: List[tuple[Path, Path]] = []

    for path in log_dir.glob("*.log"):
        if not path.is_file():
            continue
        mtime = datetime.fromtimestamp(path.stat().st_mtime)
        if mtime < threshold:
            target = archive_dir / path.name
            planned_moves.append((path, target))

    for src, dst in planned_moves:
        if dry_run:
            print(f"[DRY-RUN] 将移动：{src} -> {dst}")
        else:
            print(f"移动日志：{src} -> {dst}")
            shutil.move(src, dst)

    return planned_moves


def create_temp_workdir_example(files: Iterable[str]) -> Path:
    """
    使用临时目录进行文件操作实验的示例。

    函数会：
    1. 创建一个临时目录；
    2. 在其中写入若干测试文件；
    3. 返回该目录路径，方便你在 REPL 中继续操作。
    """
    tmp_dir = Path(tempfile.mkdtemp(prefix="learn_files_demo_"))
    for name in files:
        file_path = tmp_dir / name
        file_path.write_text(f"示例内容：{name}\n", encoding="utf-8")
    print(f"已在临时目录创建测试文件：{tmp_dir}")
    return tmp_dir


def _demo() -> None:
    """
    简单示例入口：在交互式环境中调用时，演示各函数的基本用法。

    推荐在 Python REPL 中这样使用：

    >>> from pathlib import Path
    >>> from demo_files_dirs import create_temp_workdir_example, find_files_by_suffix, move_old_logs
    >>> tmp = create_temp_workdir_example(["a.log", "b.txt", "c.log"])
    >>> find_files_by_suffix(tmp, ".log")

    日志归档示例（在自己准备的 log 目录中实验）：

    >>> log_dir = Path("/path/to/logs")
    >>> archive_dir = Path("/path/to/logs/archive")
    >>> move_old_logs(log_dir, archive_dir, days=30, dry_run=True)
    """
    print(
        "本模块主要用于配合文档进行示例学习，"
        "建议在 Python 交互式环境中按文档中的说明调用各个函数。"
    )


if __name__ == "__main__":
    _demo()

