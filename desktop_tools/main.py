#!/usr/bin/env python3
"""狗狗百宝箱 - 主入口"""

import sys
from pathlib import Path

import webview

from api import Api


# 判断是否为打包环境
def is_bundled():
    return getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")


def get_base_path():
    """获取程序基础路径"""
    if is_bundled():
        return Path(sys._MEIPASS)
    return Path(__file__).parent


def get_data_dir():
    """获取数据存储目录"""
    if is_bundled():
        # 打包后使用用户主目录下的文件夹
        home = Path.home()
        data_dir = home / ".dog_toolbox"
        data_dir.mkdir(exist_ok=True)
        return data_dir
    else:
        # 开发环境使用项目目录
        return Path(__file__).parent


def main():
    data_dir = get_data_dir()
    api = Api(data_dir)

    web_dir = get_base_path() / "web"
    webview.create_window(
        title="狗狗百宝箱",
        url=str(web_dir / "index.html"),
        js_api=api,
        width=1200,
        height=800,
        min_size=(800, 600),
    )
    webview.start(debug=False)


if __name__ == "__main__":
    main()
