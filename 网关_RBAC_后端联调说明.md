# 网关 + RBAC + 后端服务 本地联调说明

本文档说明如何在本仓库中同时启动：

- RBAC 鉴权服务（`rbac_auth_service`）
- 通用 HTTP 网关服务（`integration_gateway_service`）
- Python 后端用户与订单示例服务（`backend_user_order_service`）

并完成一条从“客户端 -> 网关 -> 后端服务”的调用链练习。

---

## 一、前置准备

1. 在仓库根目录安装依赖：

   ```bash
   pip install -r requirements.txt
   ```

2. 确保本地 Python 版本符合仓库要求（建议 3.10+）。

---

## 二、启动三个服务

### 1. 启动 RBAC 鉴权服务

1）初始化 RBAC 示例数据（如管理员账号等），在仓库根目录执行：

```bash
python rbac_auth_service/init_rbac_data.py
```

2）启动 RBAC 服务（示例命令，端口可按需要调整，例如 8001）：

```bash
uvicorn rbac_auth_service.app.main:app --reload --port 8001
```

> 具体说明可参考 `rbac_auth_service/09_项目说明.md`。

### 2. 启动 Python 后端用户与订单服务

在仓库根目录执行：

```bash
uvicorn backend_user_order_service.app.main:app --reload --port 9000
```

启动后可访问：

- 接口文档：`http://127.0.0.1:9000/docs`
- 示例接口：
  - `GET /api/users/1`
  - `POST /api/orders`

### 3. 启动通用 HTTP 网关服务

在仓库根目录执行：

```bash
uvicorn integration_gateway_service.app.main:app --reload --port 8000
```

默认情况下，网关会将下游基础地址指向：

- `GATEWAY_BACKEND_SERVICE_BASE_URL` 默认值：`http://localhost:9000`

如需显式配置，可在环境变量或 `.env` 中设置：

```env
GATEWAY_BACKEND_SERVICE_BASE_URL=http://127.0.0.1:9000
GATEWAY_RBAC_JWT_SECRET_KEY=请设置为和RBAC服务相同的SECRET_KEY
GATEWAY_RBAC_JWT_ALGORITHM=HS256
```

网关接口文档地址：

- `http://127.0.0.1:8000/docs`

---

## 三、典型调用链示例

下面以“登录获取 Token -> 通过网关查询用户并创建订单”为例，说明完整调用流程。

### 1. 在 RBAC 服务中登录获取 JWT

假设初始化脚本创建了 `alice` 用户，可以通过类似接口登录（具体路径以 RBAC 文档为准，例如 `/auth/login`）：

```bash
curl -X POST "http://127.0.0.1:8001/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "alice123"}'
```

从响应中取出 `access_token`，记为：

```text
<ACCESS_TOKEN>
```

### 2. 通过网关查询后端用户信息

调用网关的用户查询接口：

```bash
curl "http://127.0.0.1:8000/gateway/backend/users/1" \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

预期行为：

- 网关验证 JWT 是否有效；
- 网关调用后端服务 `GET /api/users/1`；
- 返回统一结构：

```json
{
  "success": true,
  "data": {
    "id": 1,
    "username": "alice",
    "full_name": "Alice Zhang"
  },
  "error": null
}
```

### 3. 通过网关创建订单

调用网关的订单创建接口（这里不直接传 `user_id`，由网关从 Token 中解析当前用户并补充）：

```bash
curl -X POST "http://127.0.0.1:8000/gateway/backend/orders" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 42, "quantity": 3}'
```

预期行为：

- 网关从 JWT payload 中读取 `sub` 作为 `user_id`；
- 组装为后端服务需要的请求体：
  - `{"user_id": <sub>, "product_id": 42, "quantity": 3}`
- 调用后端服务 `POST /api/orders`；
- 将后端返回的 `OrderOut` 包装为统一响应：

```json
{
  "success": true,
  "data": {
    "order_id": 1,
    "status": "CREATED",
    "message": "用户 1 创建了商品 42 的订单（数量：3）",
    "created_at": "2024-01-01T00:00:00Z"
  },
  "error": null
}
```

> 实际 `order_id` 和 `created_at` 值以后端服务返回为准。

---

## 四、故障与排查建议

1. **返回 401 未认证**
   - 检查是否在请求头中携带了正确的 `Authorization: Bearer <ACCESS_TOKEN>`；
   - 检查 `GATEWAY_RBAC_JWT_SECRET_KEY` 是否与 RBAC 服务实际使用的 `SECRET_KEY` 一致。

2. **返回 502 Bad Gateway**
   - 通常表示网关调用后端服务失败：
     - 检查后端服务是否已在 `9000` 端口启动；
     - 检查 `GATEWAY_BACKEND_SERVICE_BASE_URL` 配置是否正确；
     - 查看后端服务日志，确认是否有异常。

3. **用户信息不匹配或订单中的用户 ID 不正确**
   - 检查 RBAC 中 Token payload 的 `sub` 字段是否为预期的用户 ID；
   - 根据需要调整 RBAC 服务的 Token 载荷结构（例如增加 username/roles 等）。

---

## 五、后续可扩展方向（仅规划）

- 在网关中根据 Token 的角色/权限，对不同路由施加访问控制；
- 将订单创建、敏感查询等操作的审计日志写入后续的 `log_audit_service`；
- 在后端服务中引入数据库，替换当前的内存存储实现，进一步贴近真实项目场景。

