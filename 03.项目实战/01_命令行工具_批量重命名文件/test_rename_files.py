"""rename_files 脚本的基础单元测试。

测试目标：
- 确认前缀 / 后缀拼接逻辑正确；
- 确认扩展名过滤生效；
- 确认 dry_run 时不会真正重命名文件。
"""

from pathlib import Path

import pytest

import sys


def _import_rename_files():
    """从同目录动态导入 rename_files 模块，避免路径问题。"""
    current_dir = Path(__file__).resolve().parent
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))
    import rename_files  # type: ignore

    return rename_files


def test_rename_files_basic(tmp_path: Path) -> None:
    """基础场景：添加前缀 / 后缀并按序号重命名。"""
    rename_files = _import_rename_files()

    # 创建三个临时文件
    for name in ["a.txt", "b.txt", "c.txt"]:
        (tmp_path / name).write_text("demo", encoding="utf-8")

    rename_files.rename_files(tmp_path, prefix="pre_", suffix="_suf")

    names = sorted(p.name for p in tmp_path.iterdir() if p.is_file())
    assert names == [
        "001_pre_a_suf.txt",
        "002_pre_b_suf.txt",
        "003_pre_c_suf.txt",
    ]


def test_rename_files_ext_filter(tmp_path: Path) -> None:
    """只重命名指定扩展名的文件。"""
    rename_files = _import_rename_files()

    (tmp_path / "a.txt").write_text("demo", encoding="utf-8")
    (tmp_path / "b.log").write_text("demo", encoding="utf-8")

    rename_files.rename_files(tmp_path, prefix="x_", extensions=["txt"])

    names = sorted(p.name for p in tmp_path.iterdir() if p.is_file())
    # 只有 txt 被重命名，log 保持不变
    assert "001_x_a.txt" in names
    assert "b.log" in names


def test_rename_files_dry_run(tmp_path: Path) -> None:
    """dry_run 模式只打印不真正重命名。"""
    rename_files = _import_rename_files()

    file_path = tmp_path / "a.txt"
    file_path.write_text("demo", encoding="utf-8")

    rename_files.rename_files(tmp_path, prefix="x_", dry_run=True)

    # 文件名不应发生变化
    assert (tmp_path / "a.txt").is_file()


def test_rename_files_invalid_dir(tmp_path: Path) -> None:
    """目标路径不是目录时，应抛出 ValueError。"""
    rename_files = _import_rename_files()

    file_path = tmp_path / "a.txt"
    file_path.write_text("demo", encoding="utf-8")

    with pytest.raises(ValueError):
        rename_files.rename_files(file_path)

