#!/usr/bin/env python3
"""桌面工具 - 主入口"""
import sys
import os
from pathlib import Path

import webview

# 判断是否为打包环境
def is_bundled():
    return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')

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
        data_dir = home / ".local_toolbox"
        data_dir.mkdir(exist_ok=True)
        return data_dir
    else:
        # 开发环境使用项目目录
        return Path(__file__).parent

# 确保可以导入 services 模块
sys.path.insert(0, str(get_base_path()))

from api import Api


def main():
    data_dir = get_data_dir()
    api = Api(data_dir)

    web_dir = get_base_path() / "web"
    window = webview.create_window(
        title="本地工具箱",
        url=str(web_dir / "index.html"),
        js_api=api,
        width=1200,
        height=800,
        min_size=(800, 600),
    )
    webview.start(debug=False)


if __name__ == "__main__":
    main()
