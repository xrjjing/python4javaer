# Integration Gateway Service

系统对接网关服务，负责统一认证、路由转发和日志审计。

## 功能特性

- **统一认证：** JWT Token 验证，与 RBAC 服务集成
- **路由转发：** 代理下游用户服务和订单服务
- **权限控制：** 基于角色的访问控制
- **日志审计：** 自动上报关键操作日志
- **日志分析：** 集成日志侦探服务

## 技术栈

- **框架：** FastAPI
- **HTTP 客户端：** httpx
- **认证：** python-jose (JWT)
- **配置管理：** pydantic-settings
- **测试：** pytest + respx

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置环境变量

创建 `.env` 文件：

```env
GATEWAY_BACKEND_SERVICE_BASE_URL=http://localhost:9000
GATEWAY_RBAC_JWT_SECRET_KEY=your-secret-key
GATEWAY_LOG_AUDIT_BASE_URL=http://localhost:9002
GATEWAY_LOG_DETECTIVE_BASE_URL=http://localhost:9003
```

### 启动服务

```bash
uvicorn app.main:app --reload --port 8000
```

访问 API 文档：http://localhost:8000/docs

## 测试

### 运行所有测试

```bash
pytest tests/ -v
```

### 生成覆盖率报告

```bash
pytest tests/ --cov=app --cov-report=html
```

### 测试统计

- **总测试数：** 26 个
- **代码覆盖率：** 84%
- **测试策略：** 分层测试 + 端到端验证

详见 [tests/README.md](tests/README.md)

## API 端点

### 用户查询

```http
GET /gateway/backend/users/{user_id}
Authorization: Bearer <token>
```

### 创建订单

```http
POST /gateway/backend/orders
Authorization: Bearer <token>
Content-Type: application/json

{
  "user_id": 1,
  "product_id": 42,
  "quantity": 2
}
```

### 日志分析

```http
POST /gateway/log-detective/analyze
Authorization: Bearer <token>
Content-Type: application/json

{
  "log_text": "your log content"
}
```

## 项目结构

```
integration_gateway_service/
├── app/
│   ├── __init__.py
│   ├── main.py                      # 应用入口
│   ├── config.py                    # 配置管理
│   ├── dependencies.py              # 依赖注入（认证）
│   ├── schemas.py                   # 数据模型
│   ├── client_backend_service.py    # 后端服务客户端
│   ├── log_detective_client.py      # 日志侦探客户端
│   ├── log_audit_client.py          # 审计日志客户端
│   └── routers/
│       └── gateway.py               # 网关路由
└── tests/
    ├── test_client_backend_service.py
    ├── test_log_detective_client.py
    ├── test_dependencies.py
    ├── test_router_gateway.py
    └── test_e2e_smoke.py
```

## 开发指南

### 添加新路由

1. 在 `app/routers/gateway.py` 中定义路由
2. 使用 `get_current_user` 依赖进行认证
3. 使用 `get_backend_client` 获取下游客户端
4. 添加对应的测试用例

### 测试策略

- **Client 层：** 使用 `respx` Mock HTTP 响应
- **Router 层：** 使用依赖覆盖 Mock 客户端
- **E2E 测试：** 验证服务启动和路由注册

## 许可证

MIT
