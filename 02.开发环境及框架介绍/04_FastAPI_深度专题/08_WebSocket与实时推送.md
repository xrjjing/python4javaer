# 第8章：WebSocket与实时推送

## 1. WebSocket 基础

### 1.1 WebSocket vs HTTP 长轮询

| 特性 | HTTP 长轮询 | WebSocket |
|------|------------|-----------|
| 连接方式 | 短连接，反复建立 | 长连接，一次握手 |
| 通信方向 | 单向（客户端主动） | 双向（服务端可主动推送） |
| 开销 | 每次请求都有 HTTP 头 | 握手后仅传输数据帧 |
| 实时性 | 取决于轮询间隔 | 真正实时 |
| 适用场景 | 低频更新 | 高频实时通信（聊天、推送） |

### 1.2 Java 对照

| Java (Spring) | FastAPI | 说明 |
|--------------|---------|------|
| `@ServerEndpoint` (JSR-356) | `@app.websocket("/ws")` | WebSocket 端点声明 |
| `@OnOpen` / `@OnClose` | `await websocket.accept()` / `try/except WebSocketDisconnect` | 连接生命周期（捕获断开后清理资源） |
| `@OnMessage` | `await websocket.receive_text()` | 接收消息 |
| `session.getBasicRemote().sendText()` | `await websocket.send_text()` | 发送消息 |
| Spring WebSocket + STOMP | 自定义 ConnectionManager | 广播/订阅模式 |

---

## 2. FastAPI WebSocket 端点示例

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")
```

**关键点**：
- `await websocket.accept()`：必须先接受连接
- `receive_text()` / `receive_json()`：接收消息
- `send_text()` / `send_json()`：发送消息
- `WebSocketDisconnect` 异常：客户端断开时触发

---

## 3. 连接生命周期管理

### 3.1 连接管理器（支持房间/频道）

```python
from typing import Dict, Set
from fastapi import WebSocket, WebSocketDisconnect
import contextlib

class ConnectionManager:
    def __init__(self):
        # 房间 -> WebSocket 集合
        self.rooms: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room: str):
        await websocket.accept()
        if room not in self.rooms:
            self.rooms[room] = set()
        self.rooms[room].add(websocket)

    def disconnect(self, websocket: WebSocket, room: str):
        if room in self.rooms:
            self.rooms[room].discard(websocket)
            if not self.rooms[room]:
                del self.rooms[room]

    async def broadcast(self, message: str, room: str):
        """向指定房间广播消息"""
        if room in self.rooms:
            dead_sockets = set()
            for ws in self.rooms[room]:
                try:
                    await ws.send_text(message)
                except Exception:
                    dead_sockets.add(ws)
            # 清理并主动关闭失效连接
            for ws in dead_sockets:
                with contextlib.suppress(Exception):
                    await ws.close()
            self.rooms[room] -= dead_sockets

manager = ConnectionManager()

@app.websocket("/ws/{room}")
async def room_endpoint(websocket: WebSocket, room: str):
    await manager.connect(websocket, room)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"[{room}] {data}", room)
    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(websocket, room)
        with contextlib.suppress(Exception):
            await websocket.close()
```

**Java 对照**：
- Spring `SimpMessagingTemplate.convertAndSend("/topic/room", msg)` ≈ `manager.broadcast(msg, room)`
- STOMP 订阅 `/topic/room` ≈ FastAPI 房间机制

---

## 4. 心跳与保活（Ping/Pong）

```python
import asyncio
import contextlib
from fastapi import WebSocket, WebSocketDisconnect

HEARTBEAT_INTERVAL = 30  # 秒

async def heartbeat(websocket: WebSocket):
    """定期发送 ping，检测连接存活"""
    try:
        while True:
            await asyncio.sleep(HEARTBEAT_INTERVAL)
            await websocket.send_text('{"type": "ping"}')
    except Exception:
        pass

@app.websocket("/ws")
async def websocket_with_heartbeat(websocket: WebSocket):
    await websocket.accept()
    heartbeat_task = asyncio.create_task(heartbeat(websocket))
    try:
        while True:
            data = await websocket.receive_text()
            if data == '{"type": "pong"}':
                continue  # 客户端响应心跳
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        pass
    finally:
        heartbeat_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await heartbeat_task
```

**客户端示例（JavaScript）**：
```javascript
const ws = new WebSocket("ws://localhost:8000/ws");
ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (msg.type === "ping") {
        ws.send(JSON.stringify({type: "pong"}));
    }
};
```

---

## 5. 重连策略（客户端）

```javascript
class ReconnectingWebSocket {
    constructor(url, maxRetries = 5) {
        this.url = url;
        this.maxRetries = maxRetries;
        this.retries = 0;
        this.connect();
    }

    connect() {
        this.ws = new WebSocket(this.url);
        this.ws.onopen = () => {
            console.log("Connected");
            this.retries = 0;
        };
        this.ws.onclose = () => {
            if (this.retries < this.maxRetries) {
                const delay = Math.min(1000 * 2 ** this.retries, 30000);
                console.log(`Reconnecting in ${delay}ms...`);
                setTimeout(() => this.connect(), delay);
                this.retries++;
            }
        };
    }
}
```

**说明**：
- 指数退避：`2^n` 秒，最大 30 秒
- 服务端无需特殊处理，客户端自动重连

---

## 6. WebSocket 认证

### 6.1 基于 Token 的认证

```python
from fastapi import WebSocket, WebSocketDisconnect, status
from jose import jwt, JWTError

SECRET_KEY = "your-secret-key"

async def verify_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        return None

@app.websocket("/ws")
async def authenticated_websocket(websocket: WebSocket):
    # 从查询参数获取 token
    token = websocket.query_params.get("token")
    user = await verify_token(token) if token else None

    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Hello {user['sub']}: {data}")
    except WebSocketDisconnect:
        pass
```

**客户端连接**：
```javascript
const token = localStorage.getItem("access_token");
const ws = new WebSocket(`ws://localhost:8000/ws?token=${token}`);
```

**Java 对照**：
- Spring Security `@MessageMapping` + `Principal` ≈ FastAPI 手动验证 token

---

## 7. 流量控制与消息大小限制

```python
from fastapi import WebSocket, status, WebSocketDisconnect
import asyncio

MAX_MESSAGE_SIZE = 1024 * 10  # 10KB
RATE_LIMIT = 10  # 每秒最多 10 条消息

class RateLimiter:
    def __init__(self, max_rate: int):
        self.max_rate = max_rate
        self.tokens = max_rate
        self.last_update = asyncio.get_event_loop().time()

    async def acquire(self) -> bool:
        now = asyncio.get_event_loop().time()
        elapsed = now - self.last_update
        self.tokens = min(self.max_rate, self.tokens + elapsed * self.max_rate)
        self.last_update = now

        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

@app.websocket("/ws")
async def rate_limited_websocket(websocket: WebSocket):
    await websocket.accept()
    limiter = RateLimiter(RATE_LIMIT)

    try:
        while True:
            data = await websocket.receive_text()

            # 检查消息大小
            if len(data) > MAX_MESSAGE_SIZE:
                await websocket.close(code=status.WS_1009_MESSAGE_TOO_BIG)
                break

            # 检查速率限制
            if not await limiter.acquire():
                await websocket.send_text('{"error": "Rate limit exceeded"}')
                continue

            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        pass
```

---

## 8. 水平扩展（Redis Pub/Sub）

当应用部署多实例时，需要通过 Redis 实现跨实例广播：

```python
import asyncio
import aioredis
from contextlib import asynccontextmanager, suppress
from typing import Dict, Set
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

redis = None

@asynccontextmanager
async def lifespan(app):
    global redis
    redis = await aioredis.from_url("redis://localhost")
    yield
    await redis.close()

app = FastAPI(lifespan=lifespan)

class RedisConnectionManager:
    def __init__(self):
        self.connections: Dict[str, Set[WebSocket]] = {}
        self.sub_tasks: Dict[str, asyncio.Task] = {}

    async def connect(self, websocket: WebSocket, room: str):
        await websocket.accept()
        if room not in self.connections:
            self.connections[room] = set()
            # 订阅 Redis 频道
            self.sub_tasks[room] = asyncio.create_task(self._subscribe(room))
        self.connections[room].add(websocket)

    async def _subscribe(self, room: str):
        """订阅 Redis 频道，接收其他实例的消息"""
        pubsub = redis.pubsub()
        await pubsub.subscribe(f"room:{room}")
        try:
            async for message in pubsub.listen():
                if message["type"] == "message":
                    await self._broadcast_local(message["data"].decode(), room)
        finally:
            await pubsub.close()

    async def _broadcast_local(self, message: str, room: str):
        """仅向本实例的连接广播"""
        if room in self.connections:
            dead = set()
            for ws in self.connections[room]:
                try:
                    await ws.send_text(message)
                except Exception:
                    dead.add(ws)
            for ws in dead:
                with suppress(Exception):
                    await ws.close()
            self.connections[room] -= dead
            if not self.connections[room]:
                await self._cleanup_room(room)

    async def broadcast(self, message: str, room: str):
        """发布到 Redis，所有实例都会收到"""
        await redis.publish(f"room:{room}", message)

    async def disconnect(self, websocket: WebSocket, room: str):
        self.connections.get(room, set()).discard(websocket)
        if not self.connections.get(room):
            await self._cleanup_room(room)

    async def _cleanup_room(self, room: str):
        if task := self.sub_tasks.pop(room, None):
            task.cancel()
            with suppress(asyncio.CancelledError):
                await task
        self.connections.pop(room, None)

redis_manager = RedisConnectionManager()

@app.websocket("/ws/{room}")
async def redis_room(websocket: WebSocket, room: str):
    await redis_manager.connect(websocket, room)
    try:
        while True:
            data = await websocket.receive_text()
            await redis_manager.broadcast(f"[{room}] {data}", room)
    except WebSocketDisconnect:
        pass
    finally:
        await redis_manager.disconnect(websocket, room)
```

**Java 对照**：
- Spring Cloud Bus + RabbitMQ ≈ FastAPI + Redis Pub/Sub

---

## 9. 安全与合规

### 9.1 防止 XSS 攻击

```python
import html

@app.websocket("/ws")
async def safe_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # 转义 HTML 特殊字符
            safe_data = html.escape(data)
            await websocket.send_text(f"Echo: {safe_data}")
    except WebSocketDisconnect:
        pass
```

### 9.2 连接数限制

```python
from fastapi import HTTPException, status, WebSocketDisconnect

MAX_CONNECTIONS = 1000
active_connections = 0

@app.websocket("/ws")
async def limited_websocket(websocket: WebSocket):
    global active_connections
    if active_connections >= MAX_CONNECTIONS:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    try:
        await websocket.accept()
        active_connections += 1
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        pass
    finally:
        active_connections = max(active_connections - 1, 0)
```

---

## 10. 完整可运行示例

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, status
from contextlib import asynccontextmanager, suppress
import asyncio
from typing import Dict, Set
import html

# ========== 连接管理器 ==========
class ConnectionManager:
    def __init__(self):
        self.rooms: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room: str):
        await websocket.accept()
        if room not in self.rooms:
            self.rooms[room] = set()
        self.rooms[room].add(websocket)

    def disconnect(self, websocket: WebSocket, room: str):
        if room in self.rooms:
            self.rooms[room].discard(websocket)
            if not self.rooms[room]:
                del self.rooms[room]

    async def broadcast(self, message: str, room: str):
        if room in self.rooms:
            dead = set()
            for ws in self.rooms[room]:
                try:
                    await ws.send_text(message)
                except Exception:
                    dead.add(ws)
            self.rooms[room] -= dead

manager = ConnectionManager()

# ========== 心跳任务 ==========
async def heartbeat(websocket: WebSocket):
    try:
        while True:
            await asyncio.sleep(30)
            await websocket.send_text('{"type":"ping"}')
    except Exception:
        pass

# ========== 应用 ==========
@asynccontextmanager
async def lifespan(app):
    print("WebSocket server started")
    yield
    print("WebSocket server stopped")

app = FastAPI(lifespan=lifespan)

@app.websocket("/ws/{room}")
async def room_websocket(websocket: WebSocket, room: str):
    # 连接数限制
    if len(manager.rooms.get(room, set())) >= 100:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(websocket, room)
    heartbeat_task = asyncio.create_task(heartbeat(websocket))

    try:
        while True:
            data = await websocket.receive_text()

            # 消息大小限制
            if len(data) > 10240:
                await websocket.send_text('{"error":"Message too large"}')
                continue

            # 心跳响应
            if data == '{"type":"pong"}':
                continue

            # XSS 防护
            safe_data = html.escape(data)
            await manager.broadcast(f"[{room}] {safe_data}", room)

    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(websocket, room)
        heartbeat_task.cancel()
        with suppress(asyncio.CancelledError):
            await heartbeat_task

@app.get("/")
async def root():
    return {"message": "WebSocket server running. Connect to /ws/{room}"}
```

**测试客户端（HTML）**：
```html
<!DOCTYPE html>
<html>
<head><title>WebSocket Test</title></head>
<body>
    <input id="room" placeholder="Room name" value="lobby">
    <button onclick="connect()">Connect</button>
    <button onclick="disconnect()">Disconnect</button>
    <br>
    <input id="message" placeholder="Message">
    <button onclick="send()">Send</button>
    <div id="log"></div>

    <script>
        let ws = null;
        function connect() {
            const room = document.getElementById('room').value;
            ws = new WebSocket(`ws://localhost:8000/ws/${room}`);
            ws.onmessage = (e) => {
                const msg = JSON.parse(e.data);
                if (msg.type === 'ping') {
                    ws.send(JSON.stringify({type: 'pong'}));
                } else {
                    document.getElementById('log').innerHTML += `<p>${e.data}</p>`;
                }
            };
            ws.onopen = () => log('Connected');
            ws.onclose = () => log('Disconnected');
        }
        function disconnect() { ws?.close(); }
        function send() {
            const msg = document.getElementById('message').value;
            ws?.send(msg);
        }
        function log(msg) {
            document.getElementById('log').innerHTML += `<p><i>${msg}</i></p>`;
        }
    </script>
</body>
</html>
```

---

## 11. 最佳实践总结

| 实践 | 说明 |
|------|------|
| **心跳机制** | 定期 ping/pong，检测连接存活 |
| **重连策略** | 客户端指数退避重连 |
| **流量控制** | 限制消息大小和发送频率 |
| **认证授权** | 通过 token 验证身份 |
| **XSS 防护** | 转义用户输入 |
| **连接数限制** | 防止资源耗尽 |
| **水平扩展** | Redis Pub/Sub 实现跨实例广播 |
| **异常处理** | 捕获 `WebSocketDisconnect`，清理资源 |

---

## 12. Java 开发者迁移要点

| Spring WebSocket | FastAPI | 关键差异 |
|-----------------|---------|---------|
| `@ServerEndpoint` | `@app.websocket()` | 装饰器声明端点 |
| `@OnOpen` | `await websocket.accept()` | 显式接受连接 |
| `@OnMessage` | `await websocket.receive_text()` | 异步接收 |
| `session.getBasicRemote()` | `await websocket.send_text()` | 异步发送 |
| STOMP 订阅 | 自定义 ConnectionManager | 需手动实现房间/频道 |
| Spring Security | 手动验证 token | 无内置 WebSocket 认证 |
| `@MessageExceptionHandler` | `try/except WebSocketDisconnect` | 异常处理方式不同 |

**核心理念**：
- Spring WebSocket 基于注解和回调，FastAPI 基于 async/await
- Spring 有 STOMP 协议支持，FastAPI 需自行实现消息路由
- FastAPI 更轻量，适合简单实时场景；复杂场景可考虑 Socket.IO 库
