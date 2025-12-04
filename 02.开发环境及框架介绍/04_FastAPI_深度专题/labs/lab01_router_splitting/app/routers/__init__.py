"""路由集合，方便 main.py 统一导入。"""
from . import health, products, users

__all__ = ["health", "products", "users"]
