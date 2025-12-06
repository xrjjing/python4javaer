from pathlib import Path

from rename_files import rename_files


def test_rename_files_with_prefix_suffix(tmp_path: Path):
    files = [tmp_path / f"file{i}.txt" for i in range(2)]
    for f in files:
        f.write_text("demo", encoding="utf-8")

    rename_files(tmp_path, prefix="pre_", suffix="_suf", extensions=["txt"])

    renamed = sorted(p.name for p in tmp_path.iterdir())
    assert renamed == ["001_pre_file0_suf.txt", "002_pre_file1_suf.txt"]


def test_rename_files_dry_run(tmp_path: Path, capsys):
    f = tmp_path / "a.log"
    f.write_text("demo", encoding="utf-8")
    rename_files(tmp_path, dry_run=True)
    captured = capsys.readouterr()
    assert "[预览] a.log" in captured.out
