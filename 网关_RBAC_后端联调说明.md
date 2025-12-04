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

## 五、进阶练习：四服务全链路联调

> 本练习将 `log_audit_service` 也纳入，形成完整的"登录 → 管理 → 网关调用 → 审计日志查看"全链路。

### 练习目标

1. 同时启动 4 个服务
2. 通过前端登录并进行用户/角色管理
3. 通过网关调用后端服务
4. 在审计日志服务中查看操作记录

### 步骤 1：启动全部服务

在 4 个终端窗口中分别执行：

```bash
# 终端 1：RBAC 服务 (端口 8001)
python rbac_auth_service/init_rbac_data.py
uvicorn rbac_auth_service.app.main:app --reload --port 8001

# 终端 2：后端用户订单服务 (端口 9000)
uvicorn backend_user_order_service.app.main:app --reload --port 9000

# 终端 3：网关服务 (端口 8000)
uvicorn integration_gateway_service.app.main:app --reload --port 8000

# 终端 4：审计日志服务 (端口 8002)
uvicorn log_audit_service.app.main:app --reload --port 8002
```

### 步骤 2：启动前端并登录

```bash
# 终端 5：前端静态服务 (端口 5500)
cd frontend
python -m http.server 5500
```

1. 访问 `http://127.0.0.1:5500/login.html`
2. 使用 `admin` / `admin123` 登录
3. 登录成功后跳转到 `admin.html`

### 步骤 3：在 Admin Dashboard 中操作

1. **查看用户列表**：点击侧边栏"用户管理"
2. **查看角色列表**：点击侧边栏"角色管理"
3. **查看权限列表**：点击侧边栏"权限管理"
4. **创建新角色**：尝试创建一个新角色（如 `test_role`）

### 步骤 4：通过网关调用后端服务

使用获取的 Token 调用网关接口：

```bash
# 获取 Token（或从 localStorage 复制）
TOKEN="your_access_token_here"

# 查询用户
curl "http://127.0.0.1:8000/gateway/backend/users/1" \
  -H "Authorization: Bearer $TOKEN"

# 创建订单
curl -X POST "http://127.0.0.1:8000/gateway/backend/orders" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 100, "quantity": 2}'
```

### 步骤 5：查看审计日志

在 Admin Dashboard 中点击"审计日志"标签，或直接调用 API：

```bash
curl "http://127.0.0.1:8002/logs"
```

预期看到类似记录：
- 用户登录记录
- 角色/权限查询记录
- 网关调用记录（如已集成）

### 练习思考题

1. **Token 传递**：网关如何验证 Token 并提取用户身份？
2. **服务解耦**：RBAC 服务与后端服务之间没有直接依赖，如何做到的？
3. **审计完整性**：如果要记录所有网关调用，应该在哪里添加日志记录代码？
4. **错误处理**：当后端服务不可用时，网关返回什么？审计日志如何记录失败操作？

---

## 六、端到端练习：日志侦探 (Log Detective)

> 本练习演示完整的"前端 → 网关 → Python分析服务"调用链，展示Python正则表达式、文件处理等基础知识的实际应用。
>
> **服务详细说明**：见 `log_detective_service/09_项目说明.md`

### 练习目标

1. 启动日志侦探服务 (log_detective_service)
2. 通过前端界面提交日志文本
3. 后端分析日志并返回统计结果
4. 理解端到端的数据流转过程

### 步骤 1：启动日志侦探服务

在新终端窗口执行：

```bash
# 终端 6：日志侦探服务 (端口 9003)
uvicorn log_detective_service.app.main:app --reload --port 9003
```

服务启动后可访问：
- 接口文档：`http://127.0.0.1:9003/docs`
- 健康检查：`http://127.0.0.1:9003/health`

### 步骤 2：配置网关转发

确保网关配置中包含日志侦探服务地址（默认已配置）：

```env
GATEWAY_LOG_DETECTIVE_BASE_URL=http://localhost:9003
```

### 步骤 3：访问前端界面

1. 访问 `http://127.0.0.1:5500/log-detective.html`
2. 如未登录，会自动跳转到登录页
3. 登录后返回日志侦探界面

### 步骤 4：提交日志分析

1. **加载示例数据**：点击"加载示例"按钮
2. **或粘贴自己的日志**：在文本框中粘贴服务器日志
3. **点击"分析日志"**：系统将分析日志并展示结果

### 步骤 5：查看分析结果

分析完成后，界面会展示：

1. **统计摘要**：
   - 总行数
   - 错误数量
   - 警告数量

2. **可疑IP列表**：
   - IP地址
   - 出现次数
   - 风险原因

3. **关键错误列表**：
   - 错误级别
   - 错误消息
   - 行号

### 技术要点

1. **安全措施**：
   - 输入限制：最大2MB文本，最多50,000行
   - 认证保护：需要JWT Token才能访问
   - XSS防护：使用DOM API安全渲染结果

2. **Python知识点**：
   - 正则表达式：IP地址提取
   - 字符串处理：日志解析
   - 数据结构：字典统计、列表排序

3. **架构设计**：
   - 前端：log-detective.html
   - 网关：/gateway/log-detective/analyze
   - 后端：log_detective_service

### 练习思考题

1. **正则表达式**：如何修改代码以支持IPv6地址？
2. **性能优化**：如果日志文件很大，如何优化处理速度？
3. **功能扩展**：如何添加时间范围分析功能？
4. **安全加固**：为什么不支持用户自定义正则表达式？

### 当前限制说明

- 仅支持基础统计分析（不支持自定义正则）
- 关键错误仅分析前100行
- 不持久化原始日志内容
- 适用于学习和演示场景

---

## 七、后续可扩展方向（仅规划）

- 在网关中根据 Token 的角色/权限，对不同路由施加访问控制；
- 将订单创建、敏感查询等操作的审计日志写入后续的 `log_audit_service`；
- 在后端服务中引入数据库，替换当前的内存存储实现，进一步贴近真实项目场景；
- 扩展日志侦探功能：支持多种日志格式、时间范围过滤、导出报告等。

