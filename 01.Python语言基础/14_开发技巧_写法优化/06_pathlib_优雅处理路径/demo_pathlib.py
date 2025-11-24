"""pathlib 基本用法示例。"""

from pathlib import Path

base_dir = Path(".")

for path in base_dir.iterdir():
    if path.is_file():
        print(path.name, path.suffix, path.stat().st_size)


