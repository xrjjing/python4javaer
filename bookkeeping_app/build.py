#!/usr/bin/env python3
"""打包脚本 - 喵喵存金罐"""
import subprocess
import sys
import platform
import shutil
from pathlib import Path


def cleanup(root):
    """清理打包临时文件"""
    for name in ["build", "喵喵存金罐.spec"]:
        p = root / name
        if p.exists():
            if p.is_dir():
                shutil.rmtree(p)
            else:
                p.unlink()
            print(f"已清理: {p}")


def build():
    root = Path(__file__).parent
    main_py = root / "main.py"
    web_dir = root / "web"
    services_dir = root / "services"
    # PyInstaller 分隔符：Windows 用 ';'，其他平台用 ':'
    sep = ";" if platform.system() == "Windows" else ":"

    # 清理旧输出
    dist_dir = root / "dist"
    if dist_dir.exists():
        shutil.rmtree(dist_dir)

    # 基础命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onedir",
        "--windowed",
        "-y",
        "--name", "喵喵存金罐",
        # 添加前端资源
        "--add-data", f"{web_dir}{sep}web",
        # 添加 services 模块
        "--add-data", f"{services_dir}{sep}services",
        # 排除不需要的模块以减小体积
        "--exclude-module", "matplotlib",
        "--exclude-module", "numpy",
        "--exclude-module", "pandas",
        "--exclude-module", "scipy",
        "--exclude-module", "PIL",
        "--exclude-module", "cv2",
        "--exclude-module", "torch",
        "--exclude-module", "tensorflow",
        "--exclude-module", "tkinter",
        str(main_py)
    ]

    # 平台特定配置
    if platform.system() == "Darwin":
        icon_path = root / "icon.icns"
        if icon_path.exists():
            cmd.extend(["--icon", str(icon_path)])
        if platform.machine() == "arm64":
            cmd.extend(["--target-arch", "arm64"])
    elif platform.system() == "Windows":
        icon_path = root / "icon.ico"
        if icon_path.exists():
            cmd.extend(["--icon", str(icon_path)])

    print(f"执行命令: {' '.join(cmd)}")
    subprocess.run(cmd, cwd=root, check=True)

    print("\n✅ 打包完成!")
    print(f"📦 输出目录: {root / 'dist'}")

    # 清理临时文件
    cleanup(root)

    # 显示打包大小
    output_dir = dist_dir / "喵喵存金罐"
    if output_dir.exists():
        total_size = sum(f.stat().st_size for f in output_dir.rglob('*') if f.is_file())
        print(f"📊 打包大小: {total_size / 1024 / 1024:.1f} MB")


if __name__ == "__main__":
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("正在安装 PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)

    build()
