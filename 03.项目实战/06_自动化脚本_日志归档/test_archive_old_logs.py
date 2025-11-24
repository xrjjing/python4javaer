"""archive_old_logs 日志归档脚本的基础单元测试。"""

import datetime as dt
from pathlib import Path

import sys


def _import_archive():
    """动态导入 archive_old_logs 模块。"""
    current_dir = Path(__file__).resolve().parent
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))
    import archive_old_logs  # type: ignore

    return archive_old_logs


def test_find_old_logs_by_days(tmp_path: Path) -> None:
    """超过 N 天的日志文件应被正确筛选出来。"""
    archive = _import_archive()

    old_file = tmp_path / "old.log"
    new_file = tmp_path / "new.log"
    old_file.write_text("old", encoding="utf-8")
    new_file.write_text("new", encoding="utf-8")

    # 手动调整修改时间：old 提前 10 天，new 提前 1 天
    ten_days_ago = dt.datetime.now() - dt.timedelta(days=10)
    one_day_ago = dt.datetime.now() - dt.timedelta(days=1)
    for path, mtime in [(old_file, ten_days_ago), (new_file, one_day_ago)]:
        ts = mtime.timestamp()
        os_utime = __import__("os").utime  # 避免额外导入语句放到顶部
        os_utime(path, (ts, ts))

    result = archive.find_old_logs(tmp_path, days=7, exts=["log"])
    assert old_file in result
    assert new_file not in result


def test_archive_files_creates_zip(tmp_path: Path) -> None:
    """归档函数应生成包含目标文件的 zip 包。"""
    archive = _import_archive()

    f1 = tmp_path / "a.log"
    f2 = tmp_path / "b.log"
    f1.write_text("a", encoding="utf-8")
    f2.write_text("b", encoding="utf-8")

    zip_path = tmp_path / "logs.zip"
    archive.archive_files([f1, f2], zip_path)

    assert zip_path.is_file()

    from zipfile import ZipFile

    with ZipFile(zip_path, "r") as zf:
        names = set(zf.namelist())
        assert "a.log" in names
        assert "b.log" in names

