#!/usr/bin/env python3
"""喵喵存金罐 - 主入口"""
import sys
from pathlib import Path

import webview

from api import Api


def is_bundled():
    return getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")


def get_base_path():
    if is_bundled():
        return Path(sys._MEIPASS)
    return Path(__file__).parent


def get_data_dir():
    if is_bundled():
        home = Path.home()
        data_dir = home / ".meow_money"
        data_dir.mkdir(exist_ok=True)
        return data_dir
    else:
        return Path(__file__).parent


def main():
    data_dir = get_data_dir()
    api = Api(data_dir)

    web_dir = get_base_path() / "web"
    webview.create_window(
        title="喵喵存金罐",
        url=str(web_dir / "index.html"),
        js_api=api,
        width=1100,
        height=750,
        min_size=(900, 650),
    )
    webview.start(debug=False)


if __name__ == "__main__":
    main()
