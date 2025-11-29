#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络编程基础练习
练习：HTTP 客户端封装、批量健康检查、简单端口探测
"""

from __future__ import annotations

import socket
from dataclasses import dataclass
from typing import Iterable, List

import requests


print("=== 练习1：封装简单 HTTP GET ===")
"""
题目：实现 safe_get_text(url, timeout=5.0)
要求：
1. 发送 GET 请求，成功时返回文本内容（resp.text）
2. 出现网络错误或非 2xx 状态码时，返回 None，并打印错误信息
3. 不抛出异常到调用方
"""


def safe_get_text(url: str, timeout: float = 5.0) -> str | None:
    """安全地获取网页文本内容。"""
    # TODO: 在这里实现（参考 demo_network_programming.fetch_json 的写法）
    raise NotImplementedError


# 测试代码（完成后可取消注释）
# print(safe_get_text("https://httpbin.org/get"))


print("\n=== 练习2：批量服务健康检查 ===")
"""
题目：实现 check_services(urls)
要求：
1. 输入为 URL 列表
2. 对每个 URL 发送 GET 请求
3. 返回一个列表，元素为 (url, is_healthy)
   - is_healthy: bool，2xx 视为健康
4. 网络错误或超时视为不健康
"""


def check_services(urls: list[str], timeout: float = 3.0) -> list[tuple[str, bool]]:
    """批量检查服务健康状态。"""
    # TODO: 在这里实现
    raise NotImplementedError


# 测试代码（完成后可取消注释）
# urls = [
#     "https://httpbin.org/status/200",
#     "https://httpbin.org/status/500",
#     "https://not-exists.example.com",
# ]
# print(check_services(urls))


print("\n=== 练习3：简单端口探测（TCP） ===")
"""
题目：实现 simple_port_scan(host, ports)
要求：
1. 对给定 host 和端口列表尝试建立 TCP 连接
2. 若能连接，认为端口开放；否则认为关闭
3. 返回 (port, is_open) 列表
4. 每次连接应设置超时时间（例如 1 秒）

注意：
- 仅在本机或你有权限的环境中做简单实验，不要对陌生主机做端口扫描。
"""


def simple_port_scan(host: str, ports: Iterable[int], timeout: float = 1.0) -> list[tuple[int, bool]]:
    """简单端口探测（实验用）。"""
    # TODO: 使用 socket.socket / connect_ex 实现
    raise NotImplementedError


print("\n网络编程基础练习：建议在本地环境中选取可控的服务进行测试，理解网络错误与超时的行为。")

