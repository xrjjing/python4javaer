# Python 学习实践仓库（面向 Java 开发者）

本仓库用于你从 Java 开发者过渡到 Python 时的系统学习与实战练习，是你的「Python 练功房」。

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
  - **「15_进阶专题」**：正则表达式、标准库模块、文件操作、数据序列化、网络编程、多线程与多进程、异步编程入门，每个专题都包含与本仓库项目的对应关系说明。

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

- `rbac_auth_service/`  
  独立的 RBAC 认证与权限服务示例（FastAPI + SQLAlchemy + JWT + Redis 可选）：
  - 可单独运行，作为「真实项目雏形」或通用用户/权限模块的起点；
  - 详见 `rbac_auth_service/09_项目说明.md`。

- `frontend/`
  纯静态前端页面目录：
  - `index.html`：学习导航主页，包含章节导航和在线 Python 执行器（基于 Pyodide）
  - `login.html`：RBAC 登录页面，使用 OAuth2 密码模式认证
  - `admin.html`：RBAC 管理后台，支持用户/角色/权限管理和审计日志查看
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

- `网关_RBAC_后端联调说明.md`
  四服务联调指南，包含完整的端到端练习流程。

---

## 🧭 推荐学习路径

1. 把 `docs/Python学习规划_Java开发者版.md` 当作「总路线图」，先通读一遍，了解整体阶段划分。
2. 按顺序完成 `01.Python语言基础` 下的章节（至少前 9~10 章），并运行每章的 demo 脚本。
   - **每章都包含**：
     - 📖 章节说明文档（`.md`）
     - 💻 演示代码（`demo_xxx.py`）
     - ✏️ 练习代码（`practice_xxx.py`）
   - **运行示例**：
     ```bash
     # 运行第1章演示代码
     python 01.Python语言基础/01_快速上手与基本语法/demo_hello.py

     # 运行第2章练习代码
     python 01.Python语言基础/02_变量_数据类型_运算符/practice_types.py
     ```
3. 阅读 `02.开发环境及框架介绍/02.开发环境及框架介绍.md`：
   - 先掌握虚拟环境、依赖管理、项目结构；
   - 再重点看第 4 节的 Web 框架与 FastAPI 常用用法。
4. 在 `03.项目实战` 中选择项目动手：
   - 想练接口开发 → 从 `03_TODO_Web_API_FastAPI` 开始，再看 `08_系统对接_调用Java服务API`；
   - 想练脚本 / 自动化 → 先做 `01_命令行工具`、`06_自动化脚本_日志归档`；
   - 想练数据分析 → 做 `04_小型数据分析项目_销售统计`，结合 pandas。
5. **进阶：微服务联调体验**
   - 阅读 `网关_RBAC_后端联调说明.md`，启动 4 个服务 + 前端
   - 完成"五、进阶练习：四服务全链路联调"
   - 体验：登录 → 用户管理 → 网关调用 → 审计日志查看

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

本仓库包含 4 个可联调的微服务，演示完整的认证 → 网关 → 后端 → 审计链路：

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

# 终端 5：前端静态服务 (端口 5500)
cd frontend && python -m http.server 5500
```

启动后访问：
- 前端登录：`http://127.0.0.1:5500/login.html`（用户名 `admin`，密码 `admin123`）
- 管理后台：`http://127.0.0.1:5500/admin.html`
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
