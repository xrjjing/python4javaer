# RabbitMQ 消息队列实战项目

Python 学习平台 - RabbitMQ 消息队列基础教学项目

## 项目简介

本项目是一个完整的 RabbitMQ 消息队列学习案例，包含：
- 基础的生产者/消费者模式
- 前端可视化界面
- Mock 模式（离线演示）
- 真实 RabbitMQ 连接

## 功能特性

- **生产者**：发送消息到 RabbitMQ 队列
- **消费者**：从队列接收消息
- **队列监控**：实时查看队列统计信息
- **双模式**：
  - Mock 模式：前端模拟，无需后端
  - Real 模式：连接真实 RabbitMQ

## 快速开始

### 1. 启动 RabbitMQ（Docker）

```bash
cd rabbitmq-demo
docker-compose up -d
```

访问 RabbitMQ 管理界面：http://localhost:15672
- 用户名：admin
- 密码：admin123

### 2. 启动后端 API

```bash
cd backend
pip install -r requirements.txt

# Mock 模式（无需 RabbitMQ）
APP_MODE=mock uvicorn app.main:app --reload

# Real 模式（需要 RabbitMQ）
APP_MODE=real uvicorn app.main:app --reload
```

API 文档：http://localhost:8000/docs

### 3. 打开前端页面

```bash
cd frontend
python -m http.server 8080
```

访问：http://localhost:8080

## 项目结构

```
rabbitmq-demo/
├── backend/                # 后端 API
│   ├── app/
│   │   ├── main.py        # FastAPI 入口
│   │   ├── api/           # API 路由
│   │   ├── core/          # 核心配置
│   │   └── services/      # 业务逻辑
│   └── requirements.txt
├── frontend/              # 前端页面
│   └── index.html        # 主页面
├── docker-compose.yml    # RabbitMQ 配置
└── README.md
```

## API 端点

- `POST /api/queues/{queue_name}/messages` - 发送消息
- `GET /api/queues/{queue_name}/messages` - 获取消息
- `GET /api/queues/{queue_name}/stats` - 队列统计
- `GET /api/health` - 健康检查
- `GET /api/mode` - 当前模式

## 学习要点

1. **消息队列基础**
   - 生产者/消费者模式
   - 队列声明与持久化
   - 消息确认机制

2. **RabbitMQ 核心概念**
   - Connection 和 Channel
   - Queue 队列
   - Message 消息

3. **实战技能**
   - Python pika 库使用
   - FastAPI 异步编程
   - Docker 容器化部署

## 常见问题

### Q: Mock 模式和 Real 模式有什么区别？

A:
- Mock 模式：前端使用内存队列模拟，无需启动后端和 RabbitMQ，适合快速演示
- Real 模式：连接真实的 RabbitMQ 服务，体验完整的消息队列流程

### Q: 如何切换模式？

A:
- 前端：点击右上角的模式切换按钮
- 后端：修改环境变量 `APP_MODE=mock` 或 `APP_MODE=real`

### Q: 消息发送后看不到？

A:
- 检查 RabbitMQ 是否正常运行：`docker ps`
- 检查后端是否启动：访问 http://localhost:8000/health
- 查看浏览器控制台是否有错误信息

## 进阶学习

- [ ] 实现消息持久化
- [ ] 添加死信队列
- [ ] 实现延迟队列
- [ ] 使用 WebSocket 实时推送
- [ ] 添加消息优先级

## 相关资源

- [RabbitMQ 官方文档](https://www.rabbitmq.com/documentation.html)
- [pika 文档](https://pika.readthedocs.io/)
- [FastAPI 文档](https://fastapi.tiangolo.com/)
