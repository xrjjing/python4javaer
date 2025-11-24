# Python 学习实践仓库（面向 Java 开发者）

本仓库用于你从 Java 开发者过渡到 Python 时的系统学习与实战练习，是你的「Python 练功房」。

---

## 📚 仓库内容概览

- `docs/Python学习规划_Java开发者版.md`  
  详细的学习路线规划，按周拆分「语法 → 函数 → 面向对象 → 标准库 → Web 实战 → 进阶」等内容，可边学边在文档中打勾记录进度。

- （推荐）`src/`  
  放置每一阶段的练习代码、小脚本和小项目，例如：
  - `src/week01/`：基础语法与小脚本
  - `src/week02/`：函数与高级语法练习
  - `src/web/`：Web / API 实战项目

- （推荐）`tests/`  
  使用 `pytest` 的单元测试目录，用于练习工程化与测试驱动开发。

> 说明：目前仓库可能还没有 `src/` 和 `tests/` 目录，你可以在需要时按上面结构自行创建。

---

## 🚀 快速开始

### 1. 创建并激活虚拟环境（已创建可跳过第一步）

在项目根目录（即当前 README 所在目录）执行：

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

## 🧭 学习建议

1. 把 `docs/Python学习规划_Java开发者版.md` 当作「总路线图」  
   每学习一小段，就回去在文档里勾选对应自检项，并补充自己的笔记。

2. 每完成一个阶段，在 `src/` 下新建对应目录  
   例如第 1 周就建 `src/week01/`，把所有小脚本都放进去，方便后续对比自己的进步。

3. 尽量用 Python 风格（Pythonic）重写你熟悉的 Java 小例子  
   比如：日志分析、小工具脚本、简单 REST 接口等，加深对两门语言差异的理解。

---

## 📄 关于 LICENSE 与 .gitignore

- `.gitignore`：本仓库已为 Python 项目添加常用忽略规则（见根目录 `.gitignore` 文件），避免提交虚拟环境、缓存文件等。
- `LICENSE`：开源协议类型（如 MIT、Apache-2.0 等）会影响项目的开源方式和使用限制，建议你先想清楚是否要对外开源、采用哪种协议，再创建对应的 `LICENSE` 文件；如果需要，我可以根据你的选择生成完整的 LICENSE 文件内容。

