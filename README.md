# Python 学习实践仓库（面向 Java 开发者）

本仓库用于你从 Java 开发者过渡到 Python 时的系统学习与实战练习，是你的「Python 练功房」。

---

## 📑 文档导航（精简版）

- `docs/快速开始与依赖.md`：唯一上手入口（环境、依赖、服务启动、常用脚本）
- `docs/architecture.md`：微服务架构与调用关系
- `docs/Python学习规划_Java开发者版.md`：学习路线与自检清单
- `docs/Java_vs_Python_CheatSheet.md`：Java ↔ Python 对照速查
- `docs/文档导航与精简说明.md`：保留/归档文档清单
- `docs/查漏补缺清单.md`：对照廖雪峰教程的覆盖与缺口
- 前端与服务说明：`frontend/README.md`、各服务 `09_项目说明.md`

---

## 📂 仓库结构总览

- `docs/`  
  - `docs/Python学习规划_Java开发者版.md`：整体学习路线与自检清单（按「语言基础 → 标准库 → Web / 脚本 → 进阶」分周规划）。

- `01.Python语言基础/`
  针对 Java 开发者整理的语法学习笔记与小 demo，覆盖：
  - 快速上手、变量与数据类型、条件与循环；
  - 容器类型、函数、模块与包、异常与文件；
  - 面向对象、迭代器与生成器、lambda 与装饰器、命名空间与类型注解；
  - 「开发技巧 / 写法优化」中的 pathlib、logging、推导式、解包、EAFP 等 Pythonic 写法；
  - **「15_进阶专题」**：正则表达式、标准库模块、文件操作、数据序列化、网络编程、多线程与多进程、异步编程入门，每个专题都包含与本仓库项目的对应关系说明和**开放式挑战任务**。

- `docs/`
  学习规划与参考文档：
  - `Python学习规划_Java开发者版.md`：整体学习路线与自检清单
  - **`Java_vs_Python_CheatSheet.md`**：Java 开发者专属速查对照表
    - ✅ 正则表达式对比（转义规则、常用模式、高级特性）
    - ✅ 并发模型对比（GIL 详解、线程 vs 进程、asyncio vs CompletableFuture）
    - ✅ Web 框架对比（Spring Boot vs FastAPI）
    - 所有示例代码均可直接运行，经过技术审查确保准确性

- `02.开发环境及框架介绍/`  
  侧重工程化与框架：
  - 开发工具与交互环境（PyCharm、REPL、Jupyter）；
  - 虚拟环境与依赖管理（venv / pip / requirements.txt）；
  - 项目结构与代码组织（推荐的 `src/` 布局思路）；
  - Web 框架概览（Flask / Django / FastAPI）及**框架的好处**；
  - FastAPI 的最小 demo 与常用用法（路由、Pydantic 模型、依赖注入、APIRouter、中间件、测试等）；
  - 数据分析栈概览（numpy / pandas / 可视化）。

- `03.项目实战/`  
  从易到难的一组小项目，练习「用 Python 解决真实问题」：
  - `01_命令行工具_批量重命名文件`：Pathlib + argparse；
  - `02_日志分析与报表生成`：日志解析与 Counter 统计；
  - `03_TODO_Web_API_FastAPI`：使用 FastAPI + SQLite + SQLAlchemy 的 TODO API；
  - `04_小型数据分析项目_销售统计`：pandas 读取 CSV 并做聚合统计；
  - `05_简单爬虫_新闻标题抓取`：requests + BeautifulSoup；
  - `06_自动化脚本_日志归档`：zip 归档 + 定时任务思路；
  - `07_监控数据处理_指标聚合与告警`：CSV 指标聚合 + 简单告警规则；
  - `08_系统对接_调用Java服务API`：Python 网关调用 Java 服务 API。
  - `05_简单爬虫_新闻标题抓取`：基础版 requests+BS4 示例（教学用）。
  - `09_新闻爬虫_Requests_BS4`：进阶版，含离线 sample、异步 httpx、限速/robots 检查。

- `rbac_auth_service/`  
  独立的 RBAC 认证与权限服务示例（FastAPI + SQLAlchemy + JWT + Redis 可选）：
  - 可单独运行，作为「真实项目雏形」或通用用户/权限模块的起点；
  - 详见 `rbac_auth_service/09_项目说明.md`。

- `frontend/`
  纯静态前端页面目录：
  - `index.html`：学习导航主页，包含章节导航和在线 Python 执行器（基于 Pyodide）
  - `login.html`：RBAC 登录页面，使用 OAuth2 密码模式认证
  - `admin.html`：RBAC 管理后台，支持用户/角色/权限管理和审计日志查看
  - `log-detective.html`：日志侦探工具，通过网关调用日志分析服务
  - 详见 `frontend/README.md`

- `integration_gateway_service/`
  通用 HTTP 网关服务（FastAPI + httpx），演示：
  - JWT Token 验证与转发
  - 统一响应格式包装
  - 后端服务代理调用

- `backend_user_order_service/`
  Python 后端用户与订单示例服务（FastAPI），提供：
  - 用户查询接口
  - 订单创建接口
  - 配合网关服务演示完整调用链

- `log_audit_service/`
  审计日志服务（FastAPI），用于：
  - 接收和存储操作审计日志
  - 提供日志查询接口
  - 配合 admin.html 展示审计记录

- `log_detective_service/`
  日志侦探服务（FastAPI），专注于日志分析与安全检测：
  - 正则表达式实战应用（IP 提取、日志级别识别）
  - 安全编程实践（输入限制、ReDoS 防护）
  - 内存处理，不持久化原始日志
  - 配合 log-detective.html 提供日志分析功能
  - 详见 `log_detective_service/09_项目说明.md`

- `desktop_tools/`
  本地工具箱 - 桌面应用（PyWebView + HTML/CSS/JS）：
  - 轻量级本地桌面工具合集
  - 前端使用原生 HTML/CSS/JS，无框架依赖
  - 后端通过 PyWebView 提供 Python API
  - 支持深色模式、响应式布局
  - 可通过 PyInstaller 打包为独立可执行程序
  - 运行方式：`python desktop_tools/main.py`

- `bookkeeping_app/`
  喵喵存金罐 - 独立桌面应用（PyWebView + HTML/CSS/JS）：
  - 功能完整的个人记账应用
  - 支持多账本、多账户、分类预算管理
  - 收支统计、趋势分析、资产管理
  - 数据完整性保护（关联删除/迁移）
  - 预算超支预警系统
  - 深色模式、响应式设计
  - 数据本地存储，隐私安全
  - 运行方式：`python bookkeeping_app/main.py`
  - 打包方式：`python bookkeeping_app/build.py`

- `网关_RBAC_后端联调说明.md`
  五服务联调指南，包含完整的端到端练习流程。

---

## 🏗️ 系统架构总览

本仓库包含 **5 个微服务** 和 **前端页面集合**，演示完整的认证、网关、审计和业务服务调用链路。

```
                         前端 (static, 5500)
      +----------------------------------------------------+
      |  index.html   login.html   admin.html   log-detective.html
      +--------+-----------+-----------+-------------------+
               |           |           |
               |           |           | 审计日志查询
               |    登录/鉴权          v
               |           |    +-------------------------+
               |           +--> | log_audit_service :8002 |
               |                | 审计日志存储/查询        |
               |                +------------+------------+
               v                             ^
      +----------------------------+         |
      | rbac_auth_service :8001    |         | 审计日志上报
      | 认证/授权/签发 JWT         +---------+
      +----------------------------+

  log-detective.html
               |
               | /gateway/log-detective/analyze (携带 JWT)
               v
      +------------------------------+
      | integration_gateway_service  |
      |           :8000             |
      | - 校验 JWT                  |
      | - 统一转发/统一响应包装      |
      +-----------+------------------+
                  |                    \
        /api/*    |                     \ 日志分析转发
                  v                      v
     +-------------------------+   +------------------------+
     | backend_user_order_     |   | log_detective_service |
     | service :9000           |   |          :9003        |
     | 用户/订单示例服务        |   | 日志分析(内存计算)     |
     +-------------------------+   +------------------------+
```

**教学要点**：
- **login.html / admin.html**：演示"前端直接调用认证服务 + 审计服务"
- **log-detective.html**：演示"前端 → 网关 → 专用分析服务"的网关转发模式
- **integration_gateway_service**：演示"JWT 校验 + 下游服务代理 + 审计日志上报"

> 详细架构说明见 [`docs/architecture.md`](docs/architecture.md)

---

## 🧭 推荐学习路径

### 阶段一：语言基础（1-2周）

**目标**：建立准确的 Python 心智模型，避免 Java 思维定式

1. **快速启动**（必读）
   - 📖 阅读 `docs/Java_vs_Python_CheatSheet.md`，建立对比认知
   - 📖 阅读 `docs/Python学习规划_Java开发者版.md`，了解整体路线

2. **语法基础**（1-10章）
   - 按顺序完成 `01.Python语言基础` 前 10 章
   - 每章包含：📖 文档 + 💻 demo + ✏️ practice
   - 运行示例：
     ```bash
     python 01.Python语言基础/01_快速上手与基本语法/demo_hello.py
     python 01.Python语言基础/02_变量_数据类型_运算符/practice_types.py
     ```

3. **Pythonic 写法**（11-14章）
   - 重点：推导式、解包、上下文管理器、装饰器
   - 对比：Java Stream API vs Python 推导式
   - 练习：用 Pythonic 方式重写 Java 代码片段

### 阶段二：工程化与框架（1周）

**目标**：掌握 Python 项目开发工具链

1. **开发环境配置**
   - 📖 阅读 `02.开发环境及框架介绍.md`
   - 实践：虚拟环境、依赖管理、项目结构

2. **Web 框架入门**
   - 对比学习：Spring Boot vs FastAPI
   - 运行最小示例：
     ```bash
     cd 03.项目实战/03_TODO_Web_API_FastAPI
     uvicorn app.main:app --reload
     # 访问 http://127.0.0.1:8000/docs
     ```

### 阶段三：进阶专题（2-3周）

**目标**：掌握 Python 特有的高级特性

📚 **Chapter 15 进阶专题现状**：

| 专题 | 完成度 | 挑战任务 | 学习建议 |
|------|--------|----------|----------|
| ✅ 正则表达式 | 100% | 4个（初级→综合） | 先学 Java 对比，再做日志分析器 |
| ✅ 标准库模块 | 100% | - | 重点：collections、itertools、functools |
| ✅ 文件操作 | 100% | - | 对比 Java NIO，学习 pathlib |
| ✅ 数据序列化 | 100% | - | JSON、pickle、dataclass |
| ✅ 网络编程 | 100% | - | socket 基础 + HTTP 客户端 |
| ✅ 多线程与多进程 | 100% | 4个（初级→综合） | **重点：GIL 理解，先看对比文档** |
| ✅ 异步编程 | 100% | - | asyncio vs CompletableFuture |

**推荐学习顺序**：
1. **正则表达式**（必学）
   - 📖 阅读 `Java_vs_Python_CheatSheet.md#1-正则表达式对比`
   - 💻 完成挑战 1：智能日志分析器
   - 🎯 应用：`03.项目实战/02_日志分析与报表生成`

2. **并发模型**（重点）
   - 📖 阅读 `Java_vs_Python_CheatSheet.md#2-并发模型对比`
   - ⚠️ 理解 GIL：CPU密集 vs IO密集的不同选择
   - 💻 完成挑战 1-2：爬虫性能对比 + 日志分析器
   - 🎯 应用：`integration_gateway_service`（异步架构）

3. **异步编程**（现代 Python 核心）
   - 📖 学习 `15_进阶专题/07_异步编程入门`
   - 对比：asyncio vs Java CompletableFuture
   - 🎯 应用：所有微服务的 `async def` 端点

### 阶段四：项目实战（2-4周）

**选择适合你的实战路线**：

🔹 **路线 A：Web 后端开发者**
```
1. TODO API (FastAPI 基础)
   ↓
2. RBAC 认证服务 (JWT + 权限控制)
   ↓
3. 四服务联调 (完整微服务体验)
   ↓
4. 挑战：实时数据流处理引擎
```

🔹 **路线 B：脚本与自动化**
```
1. 命令行工具 (argparse + pathlib)
   ↓
2. 日志分析与归档 (正则 + 定时任务)
   ↓
3. 爬虫 (requests + BeautifulSoup)
   ↓
4. 挑战：分布式日志分析器
```

🔹 **路线 C：系统对接与集成**
```
1. 调用 Java 服务 API (httpx + 异步)
   ↓
2. 网关服务 (代理 + 鉴权)
   ↓
3. 审计日志服务 (事件收集)
   ↓
4. 挑战：智能任务调度系统
```

### 阶段五：高级进阶（持续）

**微服务全链路实战**：
1. 启动 4 个服务 + 前端（见下方快速启动）
2. 完成端到端练习：
   - 用户登录 (`login.html`)
   - 管理后台操作 (`admin.html`)
   - 网关调用后端服务
   - 审计日志查看
3. 📖 详见 `网关_RBAC_后端联调说明.md`

**开放式挑战完成清单**：
- [ ] 智能日志分析器（正则）
- [ ] 配置文件校验器（正则）
- [ ] 智能文本脱敏引擎（正则）
- [ ] 网页爬虫性能对比（并发）
- [ ] 分布式日志分析器（并发）
- [ ] 智能任务调度系统（并发）
- [ ] 实时数据流处理引擎（综合）

---

## 🎯 Java 开发者专属学习建议

### 心态调整
- ❌ 不要找"Python 版的 Spring Boot"
- ✅ 理解 Python 的"简洁哲学"和"Duck Typing"
- ✅ 接受"无需编译"和"动态类型"（但要善用类型提示）

### 关键差异速查
| 场景 | Java | Python | 参考章节 |
|------|------|--------|----------|
| 正则转义 | `"\\d+"` | `r"\d+"` | [对比文档§1](docs/Java_vs_Python_CheatSheet.md#1-正则表达式对比) |
| CPU并行 | 多线程 | 多进程 | [对比文档§2](docs/Java_vs_Python_CheatSheet.md#2-并发模型对比) |
| IO并发 | ExecutorService | asyncio | Chapter 15.7 |
| Web框架 | Spring Boot | FastAPI | [对比文档§3](docs/Java_vs_Python_CheatSheet.md#3-web-框架对比) |
| 依赖注入 | @Autowired | Depends() | 02章§4 + 对比文档§3.4 |

### 避坑指南
1. **GIL 陷阱**：CPU 密集任务不要用多线程，必须用多进程
2. **可变默认参数**：`def func(items=[])` 是共享的，会导致诡异bug
3. **浅拷贝问题**：嵌套列表需要 `copy.deepcopy()`
4. **异常处理**：Python 推崇 EAFP（先做后处理），而非 LBYL（先检查后做）

---

---

## 🌐 Web 框架与 Demo 总览

框架相关内容主要集中在：

- 文档层面：`02.开发环境及框架介绍/02.开发环境及框架介绍.md` 的「04_Web 框架概览与 FastAPI 入门」；
- 实战层面：
  - `03.项目实战/03_TODO_Web_API_FastAPI`：完整的 REST API 项目骨架（路由拆分、数据库、Pydantic 模型等）；
  - `03.项目实战/08_系统对接_调用Java服务API`：Python 网关调用 Java 系统接口的示例。

你可以直接运行以下示例体验框架的好处（自动路由、Swagger 文档、依赖注入等）：

```bash
# 运行 TODO Web API（FastAPI + SQLite）
pip install fastapi "uvicorn[standard]" sqlalchemy
cd 03.项目实战/03_TODO_Web_API_FastAPI
uvicorn app.main:app --reload
```

```bash
# 运行调用 Java 服务的网关示例（FastAPI + requests）
pip install fastapi "uvicorn[standard]" requests
cd 03.项目实战/08_系统对接_调用Java服务API
uvicorn api_gateway_example:app --reload
```

访问 `http://127.0.0.1:8000/docs` 即可在浏览器中通过 Swagger UI 调试接口。

---

## 🔗 微服务联调快速启动

本仓库包含 5 个可联调的微服务，演示完整的认证 → 网关 → 后端 → 审计 → 日志分析链路：

```bash
# 终端 1：RBAC 认证服务 (端口 8001)
python rbac_auth_service/init_rbac_data.py
uvicorn rbac_auth_service.app.main:app --reload --port 8001

# 终端 2：后端用户订单服务 (端口 9000)
uvicorn backend_user_order_service.app.main:app --reload --port 9000

# 终端 3：网关服务 (端口 8000)
uvicorn integration_gateway_service.app.main:app --reload --port 8000

# 终端 4：审计日志服务 (端口 8002)
uvicorn log_audit_service.app.main:app --reload --port 8002

# 终端 5：日志侦探服务 (端口 9003)
uvicorn log_detective_service.app.main:app --reload --port 9003

# 终端 6：前端静态服务 (端口 5500)
cd frontend && python -m http.server 5500
```

启动后访问：
- 前端登录：`http://127.0.0.1:5500/login.html`（用户名 `admin`，密码 `admin123`）
- 管理后台：`http://127.0.0.1:5500/admin.html`
- 日志侦探：`http://127.0.0.1:5500/log-detective.html`
- 各服务 API 文档：`http://127.0.0.1:<端口>/docs`

详细联调流程见 `网关_RBAC_后端联调说明.md`。

更多框架常用写法（路径参数、查询参数、请求体验证、依赖注入、APIRouter、中间件、后台任务、测试等），请参考：

- `02.开发环境及框架介绍/02.开发环境及框架介绍.md` 中 FastAPI 小节；
- `03.项目实战/03_TODO_Web_API_FastAPI/03_项目说明.md` 中对项目结构的说明。

---

## 🚀 环境准备（虚拟环境 + PyCharm）

### 1. 创建并激活虚拟环境（已创建可跳过）

在项目根目录执行：

```bash
cd /Users/xrj/PycharmProjects/learn
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
```

激活成功后，终端前缀会变成类似：

```bash
(.venv) xrj@xxx learn %
```

### 2. 在 PyCharm 中使用 `.venv`

1. 打开 `Settings / Preferences`  
2. 进入：`Project: learn` → `Python Interpreter`  
3. 选择 `Existing environment`，指向：  
   `/Users/xrj/PycharmProjects/learn/.venv/bin/python`  
4. 保存后，运行代码时会自动使用虚拟环境。

---

## 💻 代码示例说明

### 语言基础代码结构

`01.Python语言基础` 目录下每个章节都包含完整的学习材料：

```
01.Python语言基础/
├── 01_快速上手与基本语法/
│   ├── 01_快速上手与基本语法.md    # 章节说明文档
│   ├── demo_hello.py                # 演示代码
│   └── practice_basic_io.py         # 练习代码
├── 02_变量_数据类型_运算符/
│   ├── 02_变量_数据类型_运算符.md
│   ├── demo_types_ops.py
│   └── practice_types.py
...
├── 14_开发技巧_写法优化/
│   ├── 01_字符串格式化_f_string/
│   ├── 02_推导式_列表字典集合/
│   └── ...
└── 15_进阶专题/                    # 进阶主题
    ├── 01_正则表达式/              # 含与项目对应关系
    ├── 02_标准库常用模块/
    ├── 03_文件与目录操作/
    ├── 04_数据序列化/
    ├── 05_网络编程基础/
    ├── 06_多线程与多进程/
    ├── 07_异步编程入门/
    └── 15_进阶专题.md              # 综合实战练习
```

### 如何使用代码示例

1. **阅读文档** → 先看章节的 `.md` 文件，了解知识点
2. **运行demo** → 执行 `demo_xxx.py` 查看演示效果
3. **完成练习** → 参考 `practice_xxx.py` 完成练习题
4. **实战应用** → 在 `03.项目实战` 中应用所学知识

### 运行测试

项目实战部分包含完整的测试用例：

```bash
# 运行所有测试
pytest 03.项目实战/

# 运行特定项目测试
pytest 03.项目实战/03_TODO_Web_API_FastAPI/test_todo_api.py
```

---

## 🧪 关于 `src/` 与 `tests/`（可选工程化布局）

当前仓库的学习示例主要放在 `01.*` 与 `03.*` 目录中，方便按章节与项目管理。
如果你更习惯「真实项目」的工程化结构，可以在此基础上另外创建：

- `src/`：放置自己整理的通用库或更完整的项目代码，例如：
  - `src/learn_py_basics/`：把基础语法练习整理成可复用模块；
  - `src/api_fastapi_demo/`：提炼属于自己的 FastAPI 脚手架。
- `tests/`：使用 `pytest` 编写单元测试或接口测试：
  - `tests/test_*.py` 中调用 `03.项目实战` 里的代码进行自动化校验。

这两部分在 `docs/Python学习规划_Java开发者版.md` 与
`02.开发环境及框架介绍/02.开发环境及框架介绍.md` 中都有工程化结构建议，可按需采纳。

---

## 📄 关于 LICENSE 与 .gitignore

- `.gitignore`：本仓库已为 Python 项目添加常用忽略规则（见根目录 `.gitignore` 文件），避免提交虚拟环境、缓存文件等。
- `LICENSE`：开源协议类型（如 MIT、Apache-2.0 等）会影响项目的开源方式和使用限制，建议你先想清楚是否要对外开源、采用哪种协议，再创建对应的 `LICENSE` 文件；如果需要，我可以根据你的选择生成完整的 LICENSE 文件内容。
