# FastAPI 深度专题

> 面向 Java 开发者的 FastAPI 系统化深入学习模块

---

## 📖 学习路线

本模块采用渐进式学习路径，理论与实践交替，帮助 Java 开发者深入掌握 FastAPI 框架。

### 🎯 学习目标
- 掌握 FastAPI 高级路由与依赖注入模式
- 理解异步编程在 Web 框架中的应用
- 熟练使用 Pydantic 进行数据校验
- 掌握认证授权的最佳实践
- 学会编写可测试、可维护的 FastAPI 应用
- 了解性能优化与生产部署

---

## 📚 章节目录

### 基础复习
- [x] **01_快速复习与环境** - 最小示例、uvicorn/gunicorn 差异

### 核心概念（Phase 1 - 进行中）
- [x] **02_路由与依赖注入进阶** - APIRouter、Depends 高级用法、生命周期事件
- [x] **03_数据模型与校验_Pydantic2** - 校验模型、字段约束、Settings/环境变量
- [x] **04_数据库与事务** - Sync/Async SQLAlchemy、Session 管理、连接池
- [x] **05_认证与授权** - OAuth2+JWT、密码哈希、RBAC 路由保护

### 进阶特性（Phase 2）
- [x] **06_中间件与跨切面** - CORS、日志、耗时、全局异常处理、限流
- [x] **07_异步与背景任务** - BackgroundTasks、Celery/Redis、重试策略
- [x] **08_WebSocket与实时推送** - 基础示例、心跳、断线重连、Redis Pub/Sub
- [ ] **09_测试与Mock** - TestClient、依赖覆盖、Fake 外部服务

### 生产实践（Phase 3）
- [ ] **10_性能监控与运维** - Profiling、缓存策略、Prometheus、链路追踪
- [ ] **11_部署与配置** - 容器化、健康检查、滚动更新

---

## 🛠️ 实验室练习

每个实验都包含完整的代码示例、README 说明和测试用例。

| 实验 | 主题 | 对应章节 | 状态 |
|------|------|---------|------|
| lab01 | 路由拆分与模块化 | 02 | ✅ 已完成 |
| lab02 | 依赖链覆盖测试 | 02+04 | ✅ 已完成 |
| lab03 | 异步 SQLAlchemy | 04 | ⏳ 待开始 |
| lab04 | WebSocket 聊天室 | 08 | ⏳ 待开始 |
| lab05 | JWT + RBAC 实战 | 05 | ⏳ 待开始 |

---

## 🔗 与现有项目的联动

- **03_TODO_Web_API_FastAPI** - 同步 CRUD 基线，可参考异步改造
- **rbac_auth_service** - JWT + RBAC 专题的实战参考
- **integration_gateway_service** - 外部服务调用 + Fake 客户端示例
- **backend_user_order_service** - 微服务架构示例

---

## 🚀 快速开始

### 环境准备
```bash
# 确保已激活虚拟环境
source .venv/bin/activate  # macOS/Linux

# 安装依赖
pip install fastapi "uvicorn[standard]" sqlalchemy pydantic
```

### 运行示例
```bash
# 运行 lab01 路由拆分示例
cd 02.开发环境及框架介绍/04_FastAPI_深度专题/labs/lab01_router_splitting
uvicorn app.main:app --reload

# 访问 API 文档
open http://127.0.0.1:8000/docs
```

---

## 💡 学习建议

### 对 Java 开发者
- **心智模型转换**：Spring Boot 的 @Autowired ≈ FastAPI 的 Depends()
- **关键差异**：FastAPI 使用函数式依赖注入，无需复杂的容器和注解扫描
- **类型提示**：充分利用 Python 类型注解，获得类似 Java 的类型安全

### 学习节奏
1. **理论先行**：先阅读章节文档，理解核心概念
2. **对照学习**：关注 "Java vs Python" 对比部分
3. **动手实践**：完成对应的 lab 练习
4. **深入理解**：阅读项目中的实际代码（rbac_auth_service 等）

### 常见陷阱
- ⚠️ 在 async 路由中使用同步 IO 操作
- ⚠️ 每次请求创建新的数据库连接
- ⚠️ 忘记在 yield 后关闭资源
- ⚠️ 依赖链循环引用

---

## 📊 进度追踪

- [x] Phase 1 启动：创建目录结构
- [x] 完成第2章：路由与依赖注入进阶
- [ ] 完成 lab01：路由拆分练习
- [ ] 创建基础前端导航框架
- [ ] 完成 Phase 1 其他章节（03-05）
- [ ] Phase 2 进阶特性开发
- [ ] Phase 3 生产实践内容

---

## 🤝 贡献与反馈

如果您在学习过程中发现问题或有改进建议，欢迎提出反馈。

---

## 📄 许可

本模块是 [Python 学习实践仓库](../../README.md) 的一部分，遵循相同的开源协议。