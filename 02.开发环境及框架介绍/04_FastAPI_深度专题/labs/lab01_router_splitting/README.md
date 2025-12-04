# lab01_router_splitting · 路由拆分练习

## 🎯 练习目标
- 熟悉如何将单体 FastAPI 应用拆分为多个 `APIRouter`。
- 通过简单依赖注入 (`Depends`) 复用"伪数据库"。
- 为后续练习建立统一的目录结构与测试基线。

## 🧩 操作步骤
1. 安装依赖：`pip install fastapi uvicorn pytest`.
2. 进入目录：`cd "02.开发环境及框架介绍/04_FastAPI_深度专题/labs/lab01_router_splitting"`.
3. 运行应用：`uvicorn app.main:app --reload` 并访问接口。
4. 执行测试：`pytest`.
5. 阅读 `app/routers/*.py`，理解各路由如何挂载与复用依赖。

## ▶️ 运行方式
```bash
pip install fastapi uvicorn pytest

cd "02.开发环境及框架介绍/04_FastAPI_深度专题/labs/lab01_router_splitting"
uvicorn app.main:app --reload
# 另开终端:
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/users
curl http://127.0.0.1:8000/products/1
```

## ✅ 预期输出
- `GET /health` → `{"status": "ok"}`
- `GET /users` → 包含两个示例用户的列表
- `GET /users/1` → `{"id": 1, "name": "Alice", ...}`
- `GET /products` → 示例商品数组
- `GET /products/2` → `{"id": 2, "title": "Mouse", ...}`

## 🔍 验证清单
- [ ] `health` 路由无需任何依赖即可返回 OK。
- [ ] `users`、`products` 路由均使用 `get_db` 依赖共享伪数据。
- [ ] `404` 场景会返回 `{"detail": "... not found"}`。
- [ ] `pytest` 全部通过（见 `tests/test_app.py`）。
- [ ] 阅读完代码后能描述 router 拆分流程与依赖覆盖思路。
