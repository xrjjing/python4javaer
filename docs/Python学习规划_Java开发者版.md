# Java 开发者 Python 学习规划

> 适用人群：有 Java 开发经验（尤其是后端 / Web），希望系统掌握 Python 作为第二语言，用于脚本、后端服务或数据相关工作。

---

## 🥅 一、整体学习目标（6~8 周可循环迭代）

通过一个阶段性的学习路径，达成下面这些具体目标：

- 能读懂绝大多数常见 Python 项目代码（尤其是 Web / 脚本类）
- 能用 Python 独立完成：
  - 小型命令行工具（批量改名、日志分析等）
  - 简单的 Web API 服务（如 TODO 列表、用户管理）
  - 与数据库 / 外部 HTTP 服务交互
- 形成「Python 思维」：
  - 熟练使用 list / dict 等内置容器
  - 习惯用推导式、上下文管理器、with 语句等 Pythonic 写法
  - 掌握虚拟环境、依赖管理和常用调试方式

---

## ⏱ 二、推荐时间规划总览

假设你每周可投入 7~10 小时，可参考下面节奏（可按自己节奏拉长或压缩）：

- 第 1 周：语言基础 + 运行环境 + 与 Java 差异认知
- 第 2 周：容器、函数、高级语法（推导式、生成器、with 等）
- 第 3 周：面向对象、模块与包、异常与日志
- 第 4 周：虚拟环境、依赖管理、文件 / 网络 IO、标准库
- 第 5 周：选择一个 Web 框架（建议 FastAPI 或 Flask），实现一个小型 REST API 项目
- 第 6 周：根据兴趣选择进阶方向：
  - Web / 后端加强：认证、数据库、部署
  - 自动化脚本：运维脚本、办公自动化
  - 数据方向：pandas、简单可视化

后续：不断在实际项目中替换、补充 Java 之外能用 Python 更快完成的任务。

---

## 💻 三、环境准备（第 0 天）

### 1. 安装与版本

- 使用 Python 3.10+（目前生态主流，语法稳定）
- 建议：
  - macOS / Linux：用 `pyenv` 管理多版本 Python
  - Windows：可直接安装官方发行版，或用 Anaconda（偏数据方向时更方便）

### 2. 虚拟环境与依赖管理

核心理念：**每个项目一个虚拟环境**，与全局系统环境隔离。

- 在项目根目录创建虚拟环境：

  ```bash
  python -m venv .venv
  ```

- 激活虚拟环境：

  - macOS / Linux:
    ```bash
    source .venv/bin/activate
    ```
  - Windows（PowerShell）:
    ```bash
    .\.venv\Scripts\activate
    ```

- 安装依赖：

  ```bash
  pip install <package-name>
  pip freeze > requirements.txt
  ```

> 习惯：所有项目依赖写入 `requirements.txt`，方便复现和部署。

### 3. IDE / 编辑器

- 既然你使用 PyCharm，可以按如下习惯配置：
  - 为每个项目指定独立的虚拟环境解释器
  - 打开 `reformat code`、`import optimize` 等自动格式化
  - 打开类型检查 / 检查器（如 Pylance、mypy 集成等）

---

## 🧱 四、语言基础与 Java 对比（第 1 周）

学习目标：用 1 周时间完成从「看不懂 Python」到「能读能写小脚本」。

### 1. 运行方式与基本语法

- 在命令行运行：
  - `python` 进入交互模式（REPL）
  - `python main.py` 运行脚本
- 基本语法点：
  - 缩进代表代码块（默认 4 个空格，不用花括号）
  - 动态类型，无需声明类型：
    ```python
    x = 1
    x = "hello"  # 允许重新赋值为不同类型
    ```
  - 常见内置类型：
    - 数值：`int`、`float`
    - 布尔：`bool`
    - 文本：`str`
    - 容器：`list`、`tuple`、`dict`、`set`

### 2. 控制流（if / for / while）

- `if` 与 Java 相似，但不需要括号：

  ```python
  if x > 10:
      print("big")
  elif x > 5:
      print("medium")
  else:
      print("small")
  ```

- `for` 遍历可迭代对象：

  ```python
  for item in [1, 2, 3]:
      print(item)
  ```

### 3. 容器与切片（重点）

重点从 Java 的数组 / List / Map 思维迁移到 Python 的 list / dict 思维：

- 列表 `list`：
  ```python
  nums = [1, 2, 3, 4]
  nums.append(5)
  sub = nums[1:3]  # 切片：2,3
  ```

- 字典 `dict`（相当于 Java 的 `Map`）：
  ```python
  user = {"name": "Tom", "age": 18}
  print(user["name"])
  user["email"] = "tom@example.com"
  ```

### 4. 第 1 周实践任务

- 写 2~3 个小脚本：
  - 批量重命名某个目录下的文件
  - 解析一个简单的日志文件，统计错误行数
  - 从控制台读取输入，做简单计算（如 BMI 计算器）

---

## 🌀 五、函数与高级语法（第 2 周）

学习目标：掌握函数、参数风格、推导式、生成器等 Python 特色语法。

### 1. 函数与参数

- 定义与返回值：

  ```python
  def add(a, b):
      return a + b
  ```

- 默认参数 / 关键字参数：

  ```python
  def greet(name, prefix="Hi"):
      print(f"{prefix}, {name}")

  greet("Tom")
  greet("Tom", prefix="Hello")
  ```

- 可变参数：

  ```python
  def log(*args, **kwargs):
      print("args:", args)
      print("kwargs:", kwargs)
  ```

### 2. 推导式（Pythonic 写法）

- 列表推导式：

  ```python
  squares = [x * x for x in range(10) if x % 2 == 0]
  ```

- 字典推导式：

  ```python
  mapping = {str(i): i for i in range(5)}
  ```

> 习惯：在可以用推导式表达清晰意图时，优先使用推导式替代显式 `for` 构建列表。

### 3. 生成器与迭代

- 使用 `yield` 定义生成器，按需计算，节省内存：

  ```python
  def count_up_to(n):
      i = 0
      while i < n:
          yield i
          i += 1
  ```

### 4. 上下文管理器与 `with`

- 典型示例：文件操作
  ```python
  with open("data.txt", "r", encoding="utf-8") as f:
      content = f.read()
  ```

> 对比 Java：Python 倾向于用 `with` 简化 try/finally 资源释放逻辑。

### 5. 第 2 周实践任务

- 把第 1 周的脚本重构为：
  - 封装函数，减少重复
  - 使用推导式 / 生成器优化性能或可读性
  - 使用 `with` 处理文件 IO

---

## 🏗 六、面向对象与模块化（第 3 周）

学习目标：理解 Python 的类 / 对象模型，掌握模块化与包结构。

### 1. 类与对象（与 Java 的差异）

- 定义类与构造函数：

  ```python
  class User:
      def __init__(self, name, age):
          self.name = name
          self.age = age

      def greet(self):
          print(f"Hi, I'm {self.name}")
  ```

- 差异点：
  - 没有 `public/private` 关键字，使用命名约定（`_name`、`__name`）表达访问意图
  - `self` 必须作为实例方法第一个参数
  - 支持多继承，但实际项目中要谨慎使用

### 2. 模块与包

- 一个 `.py` 文件就是一个模块
- 一个包含 `__init__.py` 的目录就是一个包（现代 Python 已经不强制，但建议保留）
- 导入用 `import` / `from ... import ...`

### 3. 数据类（推荐）

- 使用 `dataclasses` 简化实体类：

  ```python
  from dataclasses import dataclass

  @dataclass
  class UserDTO:
      name: str
      age: int
  ```

### 4. 第 3 周实践任务

- 把之前的脚本拆成多个模块：
  - `models.py`：定义数据类
  - `services.py`：封装业务逻辑函数 / 类
  - `main.py`：负责参数解析、调用服务

---

## 🧰 七、标准库与常用库（第 4 周）

学习目标：掌握常用标准库和第三方库的基本使用。

### 1. 标准库重点

- `os` / `pathlib`：文件和目录操作
- `datetime`：时间与日期处理
- `logging`：日志记录（替代裸 `print`）
- `json` / `csv`：常见数据格式读写
- `subprocess`：调用系统命令（脚本自动化场景）

### 2. 必备第三方库方向建议

- HTTP 请求：`requests`
- 数据处理（可选）：`pandas`
- 命令行工具：`click` 或 `argparse`（标准库）

### 3. 在实践中学习

这一周重点通过「查文档 + 写项目」来熟悉：

- 为你的脚本加入日志记录
- 支持从 JSON / CSV 读取配置或数据
- 使用 `argparse / click` 为脚本增加命令行参数

---

## 🌐 八、Web / 后端实战（第 5 周）

学习目标：用 Python 实现一个小型 REST API 服务。

### 1. 框架选择建议

- 若你习惯 Java 的注解 + 明确的接口风格，推荐：
  - **FastAPI**：类型提示友好，文档自动生成，语法现代
- 若你更想快速写小服务：
  - **Flask**：轻量、自由度高

（任选一种深入即可，后续可再扩展到 Django 等重量级框架。）

### 2. 实战项目建议：待办事项（TODO）服务

功能点：

- 接口：
  - 创建任务：`POST /todos`
  - 查询任务列表：`GET /todos`
  - 完成任务：`PUT /todos/{id}`
  - 删除任务：`DELETE /todos/{id}`
- 数据存储：
  - 入门阶段可以先用内存 / JSON 文件
  - 进阶阶段接入 SQLite / MySQL

项目中刻意练习：

- 路由与请求 / 响应模型
- 数据验证（可借助 Pydantic）
- 日志记录与错误处理

---

## 🚀 九、第 6 周及以后：按方向进阶

你可以根据兴趣和工作方向选择其一或多条：

### 1. Web / 后端深化

- 数据库与 ORM：SQLAlchemy、Django ORM 等
- 身份认证与授权：JWT、Session
- 部署：Docker 化、部署到云服务器

### 2. 自动化脚本 / 运维

- 批量管理服务器（结合 `paramiko`、`fabric` 等）
- CI/CD 脚本（GitLab CI、GitHub Actions 中用 Python 做工具脚本）
- 日志 / 监控数据采集与解析

### 3. 数据与分析入门

- 使用 `pandas` 做数据清洗和统计
- 使用 `matplotlib` / `seaborn` 做简单可视化
- 了解 Jupyter Notebook，作为交互式实验环境

---

## 🧪 十、测试与工程实践（贯穿全程）

作为 Java 开发，你已经熟悉测试和工程化，可以把这些经验迁移到 Python：

### 1. 单元测试（pytest）

- 安装：
  ```bash
  pip install pytest
  ```
- 基本习惯：
  - 测试文件以 `test_*.py` 命名
  - 测试函数以 `test_` 开头
  - 在项目根目录执行 `pytest` 即可运行全部测试

### 2. 代码风格与静态检查

- 基本工具：
  - `black`：代码格式化
  - `isort`：import 排序
  - `flake8` / `ruff`：代码检查
  - `mypy`：可选的静态类型检查

建议将它们集成到 IDE 或 Git 钩子中，保持项目风格统一。

---

## 📌 十一、建议的学习与实践节奏

结合上面的阶段划分，可以采用下面的日常节奏：

- 每次学习循环（例如 2 小时）：
  1. 20~30 分钟：阅读资料 / 文档（语言特性 / 框架）
  2. 60~80 分钟：动手敲代码，完成一个小子任务
  3. 10 分钟：整理笔记（记录遇到的问题和解决方案）

- 每周回顾：
  - 回顾本周写过的 Python 代码，找出「不够 Pythonic」的写法并重构
  - 回答 3 个问题：
    1. 这周我新学会了哪些语言特性？
    2. 哪些地方我仍然按 Java 的习惯在写 Python？
    3. 下周我想重点提升哪一块？

---

## ✅ 十二、自检清单（可以打印出来打勾）

### 语言基础

- [ ] 能解释 list / tuple / dict / set 的区别和适用场景
- [ ] 能熟练使用切片（`seq[start:end:step]`）
- [ ] 能写出 if / for / while，并理解 for-in 的迭代机制

### 函数与高级语法

- [ ] 能使用默认参数、关键字参数、可变参数
- [ ] 能用列表 / 字典推导式重写普通 for 循环
- [ ] 理解生成器的意义，并能写出简单的 `yield` 函数

### 面向对象与模块化

- [ ] 能定义类、实例方法、类方法、静态方法
- [ ] 理解模块与包的基本结构，并能组织中小型项目
- [ ] 能用 `dataclasses` 写出简洁的数据类

### 工程实践

- [ ] 知道如何创建虚拟环境，并为项目绑定解释器
- [ ] 用 `pip` / `requirements.txt` 管理依赖
- [ ] 能编写和运行简单的 `pytest` 测试

### 项目与应用

- [ ] 至少完成 1 个命令行小工具项目
- [ ] 至少完成 1 个简单的 Web API 项目
- [ ] 用 Python 解决过一个你实际工作中的小问题

---

## 📎 十三、如何在本项目中使用这份规划

- 建议在当前项目中新建如下结构：

  ```text
  .
  ├── docs/
  │   └── Python学习规划_Java开发者版.md  # 本文件
  ├── src/                               # 练习代码（可选）
  └── tests/                             # pytest 测试（可选）
  ```

- 每完成一个阶段：
  - 在本文件中对应章节打勾或补充自己的备注
  - 在 `src/` 下建立对应阶段的示例 / 小项目目录

> 目标：把这个仓库打造成你个人的「Python 实验与演进」基地，而不仅仅是一个空项目。

