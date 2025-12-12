#!/usr/bin/env python3
"""打包脚本 - 生成 Windows .exe 和 Mac .app"""
import subprocess
import sys
import platform
import shutil
from pathlib import Path


def cleanup(root):
    """清理打包临时文件"""
    build_dir = root / "build"
    spec_file = root / "狗狗百宝箱.spec"

    if build_dir.exists():
        shutil.rmtree(build_dir)
        print(f"已删除: {build_dir}")
    if spec_file.exists():
        spec_file.unlink()
        print(f"已删除: {spec_file}")


def build():
    root = Path(__file__).parent
    main_py = root / "main.py"
    web_dir = root / "web"
    icon_path = root / "icon.icns"  # Mac图标 (可选)
    icon_ico = root / "icon.ico"    # Windows图标 (可选)

    # 清理旧的输出目录
    dist_dir = root / "dist"
    if dist_dir.exists():
        shutil.rmtree(dist_dir)

    # 基础命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onedir",
        "--windowed",
        "-y",
        "--name", "狗狗百宝箱",
        "--add-data", f"{web_dir}:web",
        str(main_py)
    ]

    # 平台特定配置
    if platform.system() == "Darwin":
        # Mac
        if icon_path.exists():
            cmd.extend(["--icon", str(icon_path)])
        # 针对 ARM64
        if platform.machine() == "arm64":
            cmd.extend(["--target-arch", "arm64"])
    elif platform.system() == "Windows":
        # Windows
        if icon_ico.exists():
            cmd.extend(["--icon", str(icon_ico)])

    print(f"执行命令: {' '.join(cmd)}")
    subprocess.run(cmd, cwd=root, check=True)

    print("\n打包完成!")
    print(f"输出目录: {root / 'dist'}")

    # 清理临时文件
    cleanup(root)


if __name__ == "__main__":
    # 确保 PyInstaller 已安装
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("正在安装 PyInstaller...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "pyinstaller"],
            check=True
        )

    build()
