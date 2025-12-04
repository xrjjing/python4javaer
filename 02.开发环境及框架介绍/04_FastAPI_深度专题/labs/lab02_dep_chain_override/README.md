# Lab02: 依赖链覆盖测试

> 配套章节：02_路由与依赖注入进阶 + 04_数据库与事务

---

## 🎯 学习目标

1. 理解多级依赖链：`Settings → Engine → Session → Repository → Route`
2. 掌握 `app.dependency_overrides` 的使用方法
3. 学会在测试中用内存数据库替换真实数据库
4. 实现 CRUD 测试不触碰真实数据库

---

## 📁 项目结构

```
lab02_dep_chain_override/
├── app/
│   ├── __init__.py
│   ├── config.py         # 配置管理（依赖链起点）
│   ├── db.py             # 数据库连接（Engine → Session）
│   ├── models.py         # ORM 模型
│   ├── repositories.py   # 仓储层（数据访问）
│   ├── deps.py           # 依赖注入组装
│   ├── main.py           # FastAPI 入口
│   └── routers/
│       └── users.py      # 用户路由（依赖链终点）
├── tests/
│   └── test_users.py     # 依赖覆盖测试
└── README.md
```

---

## 🔗 依赖链示意

```
┌─────────────┐    ┌────────────┐    ┌─────────────┐    ┌──────────────┐    ┌─────────┐
│ get_settings│ -> │ get_engine │ -> │ get_session │ -> │ get_user_repo│ -> │ Route   │
│ (Settings)  │    │ (Engine)   │    │ (Session)   │    │ (Repository) │    │ Handler │
└─────────────┘    └────────────┘    └─────────────┘    └──────────────┘    └─────────┘
      ↓                  ↓                  ↓                   ↓
   配置加载          创建连接           请求级会话          数据访问层
```

**Java 对比：**
- `Settings` ≈ `@ConfigurationProperties`
- `Engine` ≈ `DataSource`
- `Session` ≈ `EntityManager`
- `Repository` ≈ `JpaRepository`

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install fastapi uvicorn sqlalchemy pydantic-settings pytest
```

### 2. 运行应用

```bash
cd lab02_dep_chain_override
uvicorn app.main:app --reload
```

访问 http://127.0.0.1:8000/docs 查看 API 文档。

### 3. 运行测试

```bash
pytest tests/ -v
```

---

## 📝 实验步骤

### Step 1: 理解依赖链

阅读以下文件，理解依赖链的构建：

1. `app/config.py` - 配置加载（起点）
2. `app/db.py` - Engine 和 Session 创建
3. `app/deps.py` - Repository 依赖
4. `app/routers/users.py` - 路由使用依赖

### Step 2: 体验 CRUD

使用 curl 或 HTTPie 测试：

```bash
# 创建用户
curl -X POST http://127.0.0.1:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@example.com"}'

# 获取用户列表
curl http://127.0.0.1:8000/users

# 获取单个用户
curl http://127.0.0.1:8000/users/1

# 更新用户
curl -X PUT http://127.0.0.1:8000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice Updated"}'

# 删除用户
curl -X DELETE http://127.0.0.1:8000/users/1
```

### Step 3: 理解依赖覆盖

打开 `tests/test_users.py`，观察：

```python
# 1. 创建测试专用的内存数据库
TEST_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(TEST_DATABASE_URL, ...)

# 2. 禁用生产数据库初始化
app = create_app(init_db=False)

# 3. 覆盖依赖
app.dependency_overrides[get_settings] = override_get_settings
app.dependency_overrides[get_session] = override_get_session
```

**关键点：**
- `create_app(init_db=False)` 禁用生产数据库初始化
- `dependency_overrides` 是一个字典
- Key 是原依赖函数，Value 是替换函数

### Step 4: 运行测试验证

```bash
pytest tests/test_users.py -v --tb=short
```

观察输出：
- SQL 语句打印（echo=True）
- 没有创建 `lab02.db` 文件
- 所有数据在内存中

---

## ✅ 验收标准

- [ ] 测试全部通过（10 个测试用例）
- [ ] 没有生成 `lab02.db` 文件（使用内存数据库）
- [ ] 理解 `dependency_overrides` 的工作原理
- [ ] 能解释依赖链的每一环

---

## 🧪 测试用例说明

| 测试 | 说明 |
|------|------|
| `test_create_user` | 创建用户返回 201 |
| `test_create_user_duplicate_email` | 重复邮箱返回 400 |
| `test_list_users` | 获取用户列表 |
| `test_get_user` | 根据 ID 获取用户 |
| `test_get_user_not_found` | 不存在返回 404 |
| `test_update_user` | 更新用户信息 |
| `test_delete_user` | 删除用户返回 204 |
| `test_delete_user_not_found` | 删除不存在返回 404 |
| `test_dependency_override_works` | 验证依赖覆盖生效 |
| `test_health_check` | 健康检查端点 |

---

## 💡 Java 对照

| FastAPI | Spring Boot |
|---------|-------------|
| `dependency_overrides` | `@MockBean` / `@TestConfiguration` |
| 内存 SQLite | H2 内嵌数据库 |
| `Depends(get_session)` | `@Autowired EntityManager` |
| pytest fixture | `@BeforeEach` / `@AfterEach` |

---

## 🔄 扩展练习

1. **异步版本**：将 `get_session` 改为异步，使用 `async_sessionmaker`
2. **Fake Repository**：创建 `FakeUserRepository`，完全不依赖数据库
3. **分页查询**：为 `list_users` 添加分页参数，并测试边界情况
4. **事务回滚**：测试创建失败时事务是否正确回滚

---

## 📚 参考

- [FastAPI 依赖注入文档](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [SQLAlchemy 2.0 文档](https://docs.sqlalchemy.org/en/20/)
- 配套章节：`02_路由与依赖注入进阶.md`、`04_数据库与事务.md`
