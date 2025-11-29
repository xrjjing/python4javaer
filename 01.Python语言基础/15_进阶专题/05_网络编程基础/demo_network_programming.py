"""
网络编程基础示例

本模块配合《05_网络编程基础》文档使用，演示三类常见的网络场景：

1. 使用 requests 作为 HTTP 客户端调用 Web API；
2. 使用 socket 实现最小的 TCP 回声服务器与客户端；
3. 使用 http.server 快速启动一个本地 HTTP 静态文件服务。

所有示例都尽量保持简单，方便你在本地直接运行和修改。
"""

from __future__ import annotations

import os
import socket
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from typing import Any

import requests


def fetch_json(url: str, timeout: float = 5.0) -> dict[str, Any] | list[Any] | None:
    """
    发送 GET 请求并尝试解析 JSON 响应。

    :param url: 目标 URL，通常为返回 JSON 的接口地址
    :param timeout: 超时时间（秒）
    :return: 解析得到的 dict / list，或失败时返回 None
    """
    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()  # 非 2xx 会抛出异常
        return resp.json()
    except requests.RequestException as exc:
        # 在真实项目中这里应改为 logging 记录日志
        print(f"请求失败：{exc}")
        return None
    except ValueError:
        print("响应体不是合法 JSON")
        return None


def run_simple_tcp_server(host: str = "127.0.0.1", port: int = 9000) -> None:
    """
    简单的 TCP 回声服务器，仅用于本地实验。

    使用方式（示例流程）：
    1. 在一个终端中运行本函数，启动服务器；
    2. 在另一个终端中调用 tcp_echo_client 发送消息；
    3. 观察服务器端和客户端的输出。
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        # 允许服务端重启后立即复用端口，避免 "Address already in use" 报错
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((host, port))
        server_sock.listen(1)
        print(f"服务器已启动，监听 {host}:{port} ... 按 Ctrl+C 退出。")

        try:
            while True:
                conn, addr = server_sock.accept()
                with conn:
                    print(f"收到来自 {addr} 的连接")
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            print("客户端已关闭连接")
                            break
                        text = data.decode("utf-8", errors="ignore")
                        print(f"收到数据：{text!r}")
                        # 回显同样的内容
                        conn.sendall(data)
        except KeyboardInterrupt:
            print("收到中断信号，准备关闭服务器...")


def tcp_echo_client(message: str, host: str = "127.0.0.1", port: int = 9000) -> str:
    """
    连接到本地回声服务器，发送一条消息并返回响应内容。

    :param message: 要发送的文本消息
    :param host: 服务器地址（默认 127.0.0.1）
    :param port: 服务器端口（默认 9000）
    :return: 服务器返回的文本响应
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        sock.sendall(message.encode("utf-8"))
        data = sock.recv(1024)
        return data.decode("utf-8", errors="ignore")


def run_simple_http_server(
    directory: str = ".",
    host: str = "127.0.0.1",
    port: int = 8000,
) -> None:
    """
    在指定目录下启动一个简单的 HTTP 静态文件服务器。

    示例步骤：
    1. 在某个目录下准备一些测试文件（HTML/文本/图片均可）；
    2. 在该目录中运行本函数；
    3. 在浏览器访问 http://127.0.0.1:8000 查看效果。
    """
    path = Path(directory).resolve()
    if not path.is_dir():
        raise ValueError(f"目录不存在：{path}")

    os.chdir(path)
    server_address = (host, port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Serving {path} on http://{host}:{port} (Ctrl+C 退出)")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("收到中断信号，准备关闭 HTTP 服务器...")
    finally:
        httpd.server_close()


def _demo() -> None:
    """
    简单的命令行入口。

    由于网络示例通常需要在多个终端中配合运行，这里仅给出提示，
    具体调用请在 Python 交互环境或单独脚本中使用：

    >>> from demo_network_programming import fetch_json
    >>> fetch_json("https://httpbin.org/get")

    >>> from demo_network_programming import run_simple_tcp_server, tcp_echo_client
    # 终端1：run_simple_tcp_server()
    # 终端2：tcp_echo_client("hello")
    """
    print("本模块主要作为示例库使用，请在交互式环境中按文档说明调用各个函数。")


if __name__ == "__main__":
    _demo()

