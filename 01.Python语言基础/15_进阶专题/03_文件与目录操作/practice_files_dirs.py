#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件与目录操作练习
练习：Pathlib 遍历、过滤、统计、安全删除与日志归档
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


print("=== 练习1：列出目录中的文件 ===")
"""
题目：实现一个函数 list_files(root)，列出目录下的所有文件名（不含子目录）。
要求：
1. 使用 Path.iterdir() 遍历
2. 只返回文件（忽略子目录）
3. 返回按文件名排序后的列表
"""


def list_files(root: Path) -> list[str]:
    """列出目录下所有文件的文件名（排序）。"""
    # TODO: 在这里实现
    raise NotImplementedError


# 测试代码（完成后可取消注释）
# from demo_files_dirs import create_temp_workdir_example
# tmp = create_temp_workdir_example(["b.txt", "a.log", "c.md"])
# print(list_files(tmp))


print("\n=== 练习2：按文件大小过滤 ===")
"""
题目：实现 find_large_files(root, min_size_bytes)
要求：
1. 递归遍历 root 下所有文件
2. 找出大小 >= min_size_bytes 的文件
3. 返回 Path 列表，按大小从大到小排序
"""


def find_large_files(root: Path, min_size_bytes: int) -> list[Path]:
    """查找大文件。"""
    # TODO: 在这里实现
    raise NotImplementedError


# 测试代码（完成后可取消注释）
# print(find_large_files(tmp, 1))


print("\n=== 练习3：安全删除（dry-run） ===")
"""
题目：实现 delete_files(files, dry_run=True)
要求：
1. files 为 Path 列表
2. dry_run=True 时只打印将要删除的文件，不真正删除
3. dry_run=False 时真正删除文件
4. 函数返回实际删除的文件数量（dry_run 时返回 0）
"""


def delete_files(files: Iterable[Path], dry_run: bool = True) -> int:
    """安全删除文件，支持 dry-run。"""
    # TODO: 在这里实现
    raise NotImplementedError


# 测试代码（完成后可取消注释）
# deleted = delete_files([tmp / "a.log", tmp / "not_exists.txt"], dry_run=True)
# print("dry-run 删除数量：", deleted)


print("\n=== 练习4：日志归档（综合） ===")
"""
题目：补充一个简单的日志归档函数 archive_logs
假设日志文件名形如：app-2024-01-01.log

要求：
1. 只归档早于 cutoff_date（YYYY-MM-DD）的日志
2. 将这些文件移动到 archive_dir（可以使用 Path.rename）
3. 支持 dry_run 模式
4. 返回 (源, 目标) 列表

提示：
可以结合 demo_files_dirs.move_old_logs 的思路进行实现。
"""


def archive_logs(
    log_dir: Path,
    archive_dir: Path,
    cutoff_date: str,
    dry_run: bool = True,
) -> list[tuple[Path, Path]]:
    """归档早于指定日期的日志文件。"""
    # TODO: 在这里实现
    raise NotImplementedError


print("\n文件与目录操作练习：建议在单独的测试目录中练习，避免误操作真实文件。")

