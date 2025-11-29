# Web 实战学习路线与任务清单（Java 开发者版）

> 这份清单帮你把仓库里的 Web 项目变成一条「可执行的实战路线」，每一阶段都有 **具体项目 + 推荐任务**，你可以按顺序打勾完成。

配套阅读：

- 总体学习规划：`docs/Python学习规划_Java开发者版.md`
- Web 结构总览：`03.项目实战/Web_接口开发_总览.md`

---

## 一、阶段 1：FastAPI 入门与 CRUD（03_TODO）

- 对应项目：`03.项目实战/03_TODO_Web_API_FastAPI`
- 目标：熟悉 FastAPI 基本用法 + ORM + 测试，写顺一个干净的 CRUD。

### 1. 必做任务清单

- [ ] 根据 README 启动 TODO 服务，打开 `/docs` 调试 4 个接口：
  - `POST /todos/` 创建；
  - `GET /todos/` 查询；
  - `PUT /todos/{id}` 更新；
  - `DELETE /todos/{id}` 删除。
- [ ] 阅读并理解以下文件的职责：
  - `app/main.py`：应用入口与 `create_app` 模式；
  - `app/models.py`：`Todo` ORM 模型；
  - `app/schemas.py`：`TodoCreate / TodoUpdate / TodoOut`；
  - `app/routers/todos.py`：路由层如何使用 Pydantic 和 ORM；
  - `app/database.py`：SQLite 与 Session 管理。
- [ ] 运行 TODO 的测试（如果有），体会 `TestClient` 的用法。

### 2. 建议练习（动手改一点）

- [ ] 给 `Todo` 增加一个字段（例如 `priority` 或 `due_date`）：
  - 完整修改：模型 / schema / 路由 / 测试；
  - 数据库表可以直接删掉重新建（学习阶段不考虑迁移）。
- [ ] 尝试在路由中加入简单的输入校验逻辑，比如标题长度限制。

完成这一阶段后，你应该能 **独立从零搭一个小型 CRUD 服务**。

---

## 二、阶段 2：系统对接与网关思维（08_系统对接）

- 对应项目：`03.项目实战/08_系统对接_调用Java服务API`
- 目标：学会让 Python 作为「中间层 / 网关」，对接 Java 或其他语言写的服务。

### 1. 必做任务清单

- [ ] 阅读并理解：
  - `client_java_service.py`：如何封装 HTTP 客户端；
  - `api_gateway_example.py`：如何用 FastAPI 包一层统一响应结构（`ApiResponse`）；
  - `test_api_gateway_example.py`：如何用 Fake Client + `dependency_overrides` 做网关测试。
- [ ] 在不改逻辑的前提下尝试运行网关服务，并（如果你本地有 Java 服务）手动改一下 `JAVA_SERVICE_BASE_URL` 测试真实对接。

### 2. 建议练习任务

- [ ] 按照你工作中某个真实的 HTTP 接口，仿写一个新的 `JavaServiceClient` 方法：
  - 新增一个 `get_xxx` 或 `create_xxx`；
  - 在 `api_gateway_example.py` 中增加对应的 `/proxy/...` 路由；
  - 补一条测试覆盖正常与失败场景。
- [ ] 尝试在 `_handle_response` 中增加更细致的错误分类：
  - 比如针对 4xx / 5xx 做不同提示；
  - 或者解析下游返回的业务错误码，再转成统一格式。

完成这一阶段后，你应该能看懂并写出一个 **简洁的 Python 网关服务**，对接 Java 会比较顺手。

---

## 三、阶段 3：RBAC 与工程化分层（09_RBAC 基础）

- 对应项目：`rbac_auth_service/`（原 `03.项目实战/09_RBAC_用户认证与权限`，现已拆分为独立服务目录）
- 目标：掌握用户 / 角色 / 权限的基础模型，理解 Controller / Service / Repository 分层，并跑通 JWT 登录与权限控制。

### 1. 必做任务清单

- [ ] 按 `09_项目说明.md` 的指引启动服务：
  - 保持默认 SQLite 即可（或按你现在的 MySQL/Redis 配置）；
  - 执行 `python init_rbac_data.py` 初始化基础数据；
  - 使用 Swagger UI 依次调用：
    - `/auth/login`：用 `admin / admin123`、`alice / alice123` 分别登录；
    - `/users/`：分别用两个用户访问，感受权限差异；
    - `/todos/`：以 `alice` 身份创建/查看 TODO。
- [ ] 阅读并理解下列文件的职责（对照 Java 分层思维）：
  - `app/models.py`：`User / Role / Permission / Todo`；
  - `app/schemas.py`：`UserCreate / UserOut / Role* / Permission* / Todo* / APIResponse / ErrorCode`；
  - `app/security.py`：JWT 签发与 Token 黑名单；
  - `app/dependencies.py`：`get_current_user` 与 `require_permissions`；
  - `app/repositories/todo_repository.py`；
  - `app/services/todo_service.py`；
  - `app/routers/auth.py`、`users.py`、`roles.py`、`todos.py`。

### 2. 建议练习任务

- [ ] 新增一个简单权限码（例如 `profile:read`），并为用户添加一个受该权限保护的接口：
  - 在 `init_rbac_data.py` 中增加权限码并分配给 `user` 角色；
  - 在 `routers/auth.py` 或新建路由中增加一个 `/me/profile` 接口；
  - 使用 `Depends(require_permissions(\"profile:read\"))` 做控制。
- [ ] 仔细阅读并跑一遍 `test_rbac_api.py`，尝试新增一条用例：
  - 模拟没有权限的用户访问受保护接口，预期返回 403。

完成这一阶段后，你应该基本能设计和实现一个 **带用户与权限的后端服务雏形**。

---

## 四、阶段 4：Project + Task 业务建模（09_RBAC 进阶）

- 对应内容：
  - 文档：`rbac_auth_service/09_Project_业务域_说明.md`
  - 代码：`rbac_auth_service/app/models.py` 中的 `Project / Task` 及其相关 repo/service/router。
- 目标：练习一对多业务关系建模与更细粒度的权限设计。

### 1. 必做任务清单

- [ ] 通读 `09_Project_业务域_说明.md`，理解 Project 域的分层实现；
- [ ] 继续阅读文档中「Project + Task 组合建模小结」部分，对照代码找对应实现；
- [ ] 按说明启动 RBAC 服务（可使用 MySQL+Redis），在 Swagger 中实际调用：
  - `POST /projects/` 创建项目；
  - `GET /projects/` 列表；
  - `POST /projects/{project_id}/tasks/` 创建任务；
  - `GET /projects/{project_id}/tasks/` 查看任务列表；
  - `PUT /projects/{project_id}/tasks/{task_id}` 更新任务状态。

### 2. 建议练习任务

- [ ] 自己改造 `Task.status`：
  - 约定只允许 `todo/doing/done/archived`；
  - 在 `TaskUpdate` schema 中增加校验（或在 service 层做枚举检查）；
  - 更新测试，验证非法状态会返回 400/422。
- [ ] 仿照 Project + Task，再加一个子资源：
  - 例如 `Comment`（任务下的评论）或 `Tag`（项目标签）；
  - 完整走一遍：models → schemas → repositories → services → routers → 权限码 → 测试。

完成这一阶段后，你就已经具备了「设计一个小型领域模型 + RBAC 控制 + 分层实现」的完整能力。

---

## 五、阶段 5：接入真实基础设施（MySQL + Redis）

- 对应说明：`rbac_auth_service/09_项目说明.md` 第五节。
- 目标：把学到的东西放到你真实的 MySQL / Redis 上跑一遍，贴近生产环境。

### 1. 必做任务清单

- [ ] 按文档中的「使用 MySQL + Redis 的完整步骤示例」配置：
  - 为 RBAC 项目在 MySQL 创建一个专用数据库；
  - 配置 `.env` 或环境变量中的 `DATABASE_URL`、`REDIS_URL`、`SECRET_KEY`；
  - 运行 `python init_rbac_data.py` 在 MySQL 中创建表和初始数据；
  - 用 uvicorn 启动服务。
- [ ] 在 MySQL 中验证：
  - 表结构是否符合预期（User/Role/Permission/Todo/Project/Task 等）；
  - 操作接口（创建项目/任务等）时，数据是否写入对应表。
- [ ] 验证 Redis 黑名单：
  - 登录获取 Token；
  - 调用 `/auth/logout`；
  - 再访问受保护接口，确认返回 401。

### 2. 建议练习任务

- [ ] 尝试为不同环境准备不同的 `.env` 文件（本地 / 测试 / 线上），练习切换配置；
- [ ] 思考如果要把这个服务部署成生产可用，还缺哪些东西（如 logging、metrics、health 检查），并列一个 TODO 清单。

---

## 六、如何使用这份清单

建议的使用方式：

- 把本文件当成「路线图 + 打勾清单」：
  - 每完成一个小任务就在前面的 `[ ]` 改成 `[x]`；
  - 遇到卡住的地方，在旁边加一行注释记录问题。
- 和 `docs/Python学习规划_Java开发者版.md` 搭配使用：
  - 总规划帮你看「大图」：语言 → 环境 → Web → 工程；
  - 本清单帮你把 Web 线的实战拆成一个个可执行的小目标。

当你把这些任务都打勾之后，基本就可以说：  
「我不仅会用 Python 写小脚本，还能像写 Java 项目一样设计后端结构和权限系统。」👍
