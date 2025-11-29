# Web 接口开发总览（FastAPI 主线）

> 这份文档帮你把和 Web/API 相关的项目串成一条清晰的学习路线，从最简单的 TODO API，到网关对接 Java 服务，再到带完整 RBAC 的用户/权限系统。

## 一、三阶段 Web 学习路线

你可以把当前仓库中的 Web 相关项目理解为三个阶段：

1. **入门阶段：学会写一个干净的 REST API**
   - 项目：`03_TODO_Web_API_FastAPI`
   - 目标：掌握 FastAPI 的路由、请求体/响应体、Pydantic 模型、简单持久化（SQLite+SQLAlchemy）与基础测试。

2. **进阶阶段：学会作为「网关」对接其他系统**
   - 项目：`08_系统对接_调用Java服务API`
   - 目标：将 Python 服务作为中间层，与 Java/其他语言写的服务通过 HTTP 交互，练习 HTTP 客户端封装、错误处理、对外暴露更友好的接口。

3. **工程阶段：引入用户 / 角色 / 权限的 RBAC 模块**
   - 项目：`09_RBAC_用户认证与权限`
   - 目标：在 FastAPI 中实现一套完整的 RBAC 模型（用户/角色/权限）、JWT 登录、统一响应结构，并用 TODO 作为受控资源示例，这已经是一个真实项目的雏形。

推荐顺序：**03 → 08 → 09**，每一步都在前一步的基础上增加真实项目中经常遇到的“复杂度维度”。

---

## 二、各项目的典型结构（和 Java 分层的关系）

### 1. TODO Web API（03_TODO_Web_API_FastAPI）

路径：`03.项目实战/03_TODO_Web_API_FastAPI`

结构（简化）：

```text
app/
├── main.py         # 应用入口（create_app）
├── database.py     # SQLite + Session 管理
├── models.py       # Todo ORM 模型
├── schemas.py      # Todo Pydantic 模型
└── routers/
    └── todos.py    # Todo 路由
```

类比 Java：

- `routers/todos.py` ≈ Controller
- `schemas.py` ≈ DTO（请求/响应对象）
- `models.py` + `database.py` ≈ Entity + 基础 Repository

特点：

- 体量小、结构简单，适合「纯 Python 视角」先把 CRUD 写顺手；
- 没有用户概念，也没有权限控制，更偏学习用途。

### 2. 调用 Java 服务的网关（08_系统对接_调用Java服务API）

路径：`03.项目实战/08_系统对接_调用Java服务API`

特点：

- 重点在于 HTTP 客户端封装：`client_java_service.py`
- FastAPI 作为“前门”，把 Java 服务的接口包装成更友好的 REST API；
- 练习：超时、错误处理、对下游异常的转换（例如下游 500 转成上游可识别的错误码）。

类比 Java：

- FastAPI 路由层依然是 Controller；
- HTTP 客户端可以看作「DAO/Repository 声明的是远程资源」；
- 如果规模继续变大，可以仿照 `09_RBAC_用户认证与权限` 的结构抽 service 层。

### 3. RBAC 用户认证与权限（09_RBAC_用户认证与权限）

路径：`rbac_auth_service/`（已从 `03.项目实战` 拆分为独立服务目录）

结构（核心部分，省略部分文件）：

```text
rbac_auth_service/
├── 09_项目说明.md          # 项目目标/模型关系/运行方式说明
├── 09_Project_业务域_说明.md # Project/Task 业务域分层说明
├── init_rbac_data.py       # 初始化 admin / alice / 角色 / 权限
├── test_rbac_api.py        # 基础接口测试
└── app/
    ├── main.py             # 应用入口 + 全局异常处理（统一响应格式）
    ├── config.py           # 配置（DATABASE_URL / REDIS_URL / SECRET_KEY 等）
    ├── database.py         # 数据库引擎与 Session 管理（SQLite / MySQL）
    ├── models.py           # User / Role / Permission / Todo / Project / Task ORM 模型
    ├── schemas.py          # Pydantic 模型 + APIResponse / ErrorCode
    ├── security.py         # 密码哈希、JWT、Token 黑名单（Redis/内存）
    ├── dependencies.py     # 当前用户 / RBAC 检查依赖（类似 filter/interceptor）
    ├── repositories/       # Repository 层（持久化细节）
    ├── services/           # Service 层（业务组合逻辑）
    └── routers/            # API 路由（Controller）
        ├── auth.py         # 登录 / 当前用户 / 登出
        ├── users.py        # 用户管理（仅 admin）
        ├── roles.py        # 角色/权限管理
        ├── todos.py        # 受 RBAC 控制的 TODO
        ├── projects.py     # Project 业务域
        └── tasks.py        # Task 子资源（挂在 Project 下）
```

和 Java 分层的对应关系：

- `routers/*` → Controller / API 层
- `schemas.py` → DTO/VO（请求/响应对象 + 通用响应封装）
- `models.py` + `database.py` → Entity + DataSource/EntityManager
- `repositories/*` → Repository 层（数据访问层）
- `services/*` → Service 层（业务逻辑）
- `security.py` + `dependencies.py` → 安全 / 权限 / 类似 Filter/Interceptor 的职责

这个项目是你问到的「能不能像 Java 一样按模块分层」的直接实现：  
现在已经具备 Controller → Service → Repository 的结构，并且为后续继续拆分（更多领域服务）留出了自然演进空间。

---

## 三、从简单到复杂：三个 Web 项目如何联动学习

### 第一阶段：掌握 FastAPI + ORM + 测试基础（03_TODO）

- 目标：不用关心用户/权限，只要把一个干净的 REST API 写顺手；
- 建议：
  - 理解 `app.main.create_app()` 的模式；
  - 熟悉 Pydantic 模型与 SQLAlchemy 模型的转换（通过 `orm_mode`）；
  - 运行 `test_todo_api.py`，体会如何用 TestClient 测 API。

### 第二阶段：学会做「中间层 / 网关」（08_系统对接）

- 目标：从“只操作数据库”升级为“对接其他系统”；
- 重点：HTTP 客户端封装 + 错误处理 + 对外接口设计；
- 建议：
  - 把这套调用 Java 服务的思路迁移到你工作里的某个真实 HTTP 对接场景（比如对接内部某个服务）。

### 第三阶段：引入用户 / 权限，写出「可以作为基础模块复用」的服务（09_RBAC）

- 目标：不只是写接口，而是能设计一个可复用的「用户 + 权限」模块；
- 重点：
  - RBAC 模型（User / Role / Permission）和表结构；
  - JWT 认证 + Token 黑名单 + 权限依赖（require_permissions 等）；
  - 统一响应格式（APIResponse + ErrorCode）与全局异常处理；
  - Controller → Service → Repository 的分层结构。
- 建议：
  1. 跑一遍 `init_rbac_data.py`，用 Swagger 验证登录/权限流程；
  2. 读一遍 `项目结构说明.md`，对照 Java 分层在脑中建立“等价映射”；
  3. 自己扩展一个小资源（比如 Project / Order），完整走一遍：
     - models → schemas → repositories → services → routers → 权限码。

---

## 四、后续可以如何继续进化结构

当你习惯了 RBAC 项目的结构之后，想进一步靠近「生产项目」可以做：

1. **把 service/repository 的模式复制到其他 Web 项目中**
   - 例如对 08 网关项目也抽出 repositories/services，形成统一的工程风格。

2. **提炼通用的“基础模块”**
   - 比如把 RBAC 里的 User/Role/Permission 相关逻辑提炼成一个可被多个服务引用的包（类似 Java 里的 common-auth 模块）。

3. **加上部署 / 配置 / logging / metrics 等工程细节**
   - 这部分我们会放在 Web 线的后续章节（如容器化、健康检查、结构化日志等）逐步补上。

---

## 五、你可以按什么顺序来学这条 Web 线？

一个实际可执行的路径建议：

1. 完整走一遍 `03_TODO_Web_API_FastAPI`（包含测试）；  
2. 完整走一遍 `08_系统对接_调用Java服务API`（让 Python 作为 Java 的前门）；  
3. 把 `09_RBAC_用户认证与权限`（代码目录 `rbac_auth_service/`）当作一个“真实服务雏形”，反复阅读与动手：
   - 先从 demo 跑通流程；
   - 再做小改动（添加权限、添加资源）；
   - 最后尝试用它作为基础模块，保护其他服务的接口。

到这一步，你在 Python Web 线上的能力已经远超过「只会写 CRUD」，而是有一套可迁移到真实工作中的结构化思维。+
