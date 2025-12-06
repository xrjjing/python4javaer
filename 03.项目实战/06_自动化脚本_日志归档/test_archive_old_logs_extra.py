import datetime as dt
from pathlib import Path

from archive_old_logs import archive_files, find_old_logs


def test_find_old_logs_filters_by_days(tmp_path: Path):
    old = tmp_path / "old.log"
    new = tmp_path / "new.log"
    old.write_text("old", encoding="utf-8")
    new.write_text("new", encoding="utf-8")

    yesterday = dt.datetime.now() - dt.timedelta(days=2)
    now = dt.datetime.now()
    old_mtime = yesterday.timestamp()
    new_mtime = now.timestamp()
    import os

    os.utime(old, (old_mtime, old_mtime))
    os.utime(new, (new_mtime, new_mtime))

    result = find_old_logs(tmp_path, days=1, exts=["log"])
    assert old in result and new not in result


def test_archive_files_creates_zip(tmp_path: Path):
    f1 = tmp_path / "a.log"
    f2 = tmp_path / "b.log"
    f1.write_text("a", encoding="utf-8")
    f2.write_text("b", encoding="utf-8")
    archive_path = tmp_path / "logs.zip"

    archive_files([f1, f2], archive_path)

    import zipfile

    with zipfile.ZipFile(archive_path, "r") as zf:
        names = zf.namelist()
        assert "a.log" in names and "b.log" in names
