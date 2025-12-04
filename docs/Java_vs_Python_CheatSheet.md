# Java vs Python 速查对照表

> **面向人群**：熟悉 Java 的开发者，希望快速掌握 Python 核心差异
> **目标**：通过对比学习，建立准确的 Python 心智模型，避免常见陷阱

---

## 📚 目录

1. [正则表达式对比](#1-正则表达式对比)
2. [并发模型对比](#2-并发模型对比)
3. [Web 框架对比](#3-web-框架对比)
4. [快速参考表](#4-快速参考表)

---

## 1. 正则表达式对比

### 1.1 核心差异总览

| 特性 | Java (`java.util.regex`) | Python (`re` 模块) |
|------|--------------------------|-------------------|
| **字符串转义** | 双重转义：`"\\d"` | 原始字符串：`r"\d"` |
| **编译对象** | `Pattern.compile()` | `re.compile()` |
| **匹配方法** | `Matcher.matches()` / `find()` | `re.match()` / `search()` / `findall()` |
| **替换** | `Matcher.replaceAll()` | `re.sub()` |
| **分组提取** | `Matcher.group(1)` | `match.group(1)` |
| **默认行为** | `.` 不匹配换行符 | `.` 不匹配换行符（需 `re.DOTALL`） |

### 1.2 转义规则详解

**Java 的痛点**：字符串字面量需要转义反斜杠

```java
// Java: 双重转义
String pattern = "\\d{3}-\\d{4}";  // 实际正则：\d{3}-\d{4}
Pattern p = Pattern.compile(pattern);
```

**Python 的优势**：原始字符串（Raw String）

```python
import re  # 所有正则操作都需要导入 re 模块

# Python: 原始字符串
pattern = r"\d{3}-\d{4}"  # 直接表达正则
regex = re.compile(pattern)
```

> **Java 开发者易错点**：忘记在 Java 中双重转义 `\`，导致运行时错误
>
> **注意**：以下所有 Python 示例均默认已导入 `re` 模块

### 1.3 常用模式对照

#### 示例 1：邮箱校验

**Java 实现**：
```java
import java.util.regex.*;

public class EmailValidator {
    private static final String EMAIL_PATTERN =
        "^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$";

    public static boolean isValidEmail(String email) {
        Pattern pattern = Pattern.compile(EMAIL_PATTERN);
        Matcher matcher = pattern.matcher(email);
        return matcher.matches();
    }

    public static void main(String[] args) {
        System.out.println(isValidEmail("user@example.com"));  // true
        System.out.println(isValidEmail("invalid-email"));     // false
    }
}
```

**Python 实现**：
```python
import re

# 使用原始字符串，无需双重转义
EMAIL_PATTERN = r"^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

def is_valid_email(email: str) -> bool:
    return re.match(EMAIL_PATTERN, email) is not None

# 测试
print(is_valid_email("user@example.com"))  # True
print(is_valid_email("invalid-email"))     # False
```

**关键差异**：
- Java `matcher.matches()` 要求**整串匹配**，等价于 Python 的 `re.fullmatch()`
- Python `re.match()` 只从字符串**开头**尝试匹配，等价于 Java 的 `matcher.lookingAt()`
- 本示例使用了 `^` 和 `$` 锚定，因此 `re.match()` 与 `re.fullmatch()` 效果相同

**Java vs Python 匹配方法对照**：
- 整串匹配：`matcher.matches()` ↔ `re.fullmatch()`
- 从开头匹配：`matcher.lookingAt()` ↔ `re.match()`
- 查找首个匹配：`matcher.find()` ↔ `re.search()`

#### 示例 2：日志解析（分组提取）

**任务**：从日志中提取时间戳、级别、消息

```
示例日志：2025-01-15 10:23:45 [ERROR] Database connection failed
```

**Java 实现**：
```java
String log = "2025-01-15 10:23:45 [ERROR] Database connection failed";
String pattern = "(\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}) \\[([A-Z]+)\\] (.+)";

Matcher matcher = Pattern.compile(pattern).matcher(log);
if (matcher.matches()) {
    String timestamp = matcher.group(1);  // "2025-01-15 10:23:45"
    String level = matcher.group(2);      // "ERROR"
    String message = matcher.group(3);    // "Database connection failed"
}
```

**Python 实现**：
```python
import re

log = "2025-01-15 10:23:45 [ERROR] Database connection failed"
pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[([A-Z]+)\] (.+)"

match = re.match(pattern, log)
if match:
    timestamp, level, message = match.groups()  # 直接解包
    # timestamp: "2025-01-15 10:23:45"
    # level: "ERROR"
    # message: "Database connection failed"
```

**关键差异**：
- Python 的 `match.groups()` 返回元组，可直接解包
- Java 需逐个调用 `group(index)`

### 1.4 高级特性对比

#### 前瞻断言（Lookahead）

**任务**：提取密码中至少包含一个数字的字符串

**Java**：
```java
String password = "Abc123";
boolean hasDigit = password.matches("(?=.*\\d).+");  // true
```

**Python**：
```python
password = "Abc123"
has_digit = bool(re.match(r"(?=.*\d).+", password))  # True
```

#### 懒惰量词（Lazy Quantifiers）

**任务**：提取 HTML 标签中的内容

```python
html = "<div>First</div><div>Second</div>"

# 贪婪匹配（错误）：匹配到最后一个 </div>
greedy = re.findall(r"<div>(.+)</div>", html)
print(greedy)  # ['First</div><div>Second']

# 懒惰匹配（正确）：尽可能少匹配
lazy = re.findall(r"<div>(.+?)</div>", html)
print(lazy)  # ['First', 'Second']
```

### 1.5 常见陷阱

| 陷阱 | Java | Python | 说明 |
|------|------|--------|------|
| **忘记转义 `.`** | `"\\."` | `r"\."` | `.` 在正则中匹配任意字符 |
| **`\b` 词边界** | `"\\bword\\b"` | `r"\bword\b"` | Java 中 `\b` 在字符串中是退格符 |
| **多行模式** | `Pattern.MULTILINE` | `re.MULTILINE` | 影响 `^` 和 `$` 的行为 |

---

## 2. 并发模型对比

### 2.1 核心概念对齐

| 概念 | Java | Python | 适用场景 |
|------|------|--------|----------|
| **线程** | `Thread` / `Runnable` | `threading.Thread` | IO 密集型（Python 受 GIL 限制） |
| **线程池** | `ExecutorService` | `ThreadPoolExecutor` / `ProcessPoolExecutor` | 管理线程/进程生命周期 |
| **进程（CPU并行）** | `ForkJoinPool` / 多线程 | `multiprocessing.Process` / `ProcessPoolExecutor` | CPU 密集型 |
| **进程（外部调用）** | `ProcessBuilder` | `subprocess` | 启动外部程序 |
| **异步** | `CompletableFuture` | `asyncio` | 高并发 IO（协程） |
| **锁** | `synchronized` / `ReentrantLock` | `threading.Lock` | 保护共享资源 |
| **原子操作** | `AtomicInteger` | 无内置原子类（需使用锁或进程安全容器） | 简单共享状态/跨进程计数 |

### 2.2 GIL（全局解释器锁）详解

**什么是 GIL？**
Python（CPython 实现）中的全局解释器锁，确保同一时刻只有一个线程执行 Python 字节码。

**对 Java 开发者的影响**：

| 场景 | Java | Python |
|------|------|--------|
| **CPU 密集型** | 多线程可利用多核 | 多线程**无法**利用多核，需用 `multiprocessing` |
| **IO 密集型** | 多线程有效 | 多线程有效（IO 时释放 GIL） |

**示例对比**：

**Java（CPU 密集型）**：
```java
// 计算质数 - 多线程可利用多核
ExecutorService executor = Executors.newFixedThreadPool(4);
List<Future<Integer>> futures = new ArrayList<>();

for (int i = 0; i < 4; i++) {
    int start = i * 25000;
    futures.add(executor.submit(() -> countPrimes(start, start + 25000)));
}

int total = futures.stream().mapToInt(f -> f.get()).sum();
executor.shutdown();
```

**Python（CPU 密集型 - 多线程失效）**：
```python
import threading

# ❌ 错误：多线程在 CPU 密集型任务下无法加速
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def count_primes_in_range(start, end, result_list, index):
    """计算 [start, end) 范围内的素数个数"""
    count = 0
    for n in range(start, end):
        if is_prime(n):
            count += 1
    result_list[index] = count

# 使用 args 参数避免闭包陷阱
threads = []
results = [0] * 4

for i in range(4):
    start = i * 25000
    end = (i + 1) * 25000
    thread = threading.Thread(
        target=count_primes_in_range,
        args=(start, end, results, i)  # ✅ 正确：使用参数传递，避免闭包
    )
    threads.append(thread)
    thread.start()

for t in threads:
    t.join()

total = sum(results)
# ❌ 即使代码逻辑正确，性能仍与单线程相同（GIL 限制）！
```

> **重要提示**：此示例虽然逻辑正确，但由于 GIL 的存在，多线程无法利用多核。性能不会比单线程快。

**Python（CPU 密集型 - 正确方案：多进程）**：
```python
from multiprocessing import Pool

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def count_primes_in_range(start, end):
    """计算 [start, end) 范围内的素数个数"""
    count = 0
    for n in range(start, end):
        if is_prime(n):
            count += 1
    return count

# ⚠️ Windows 下必须使用 if __name__ == "__main__" 保护
if __name__ == "__main__":
    with Pool(4) as pool:
        ranges = [(i * 25000, (i + 1) * 25000) for i in range(4)]
        results = pool.starmap(count_primes_in_range, ranges)
    total = sum(results)
    print(f"找到 {total} 个素数")
    # ✅ 可以利用多核，性能提升明显
```

> **关键说明**：
> - Python 多进程可以绕过 GIL，真正利用多核 CPU
> - Windows 下必须使用 `if __name__ == "__main__":` 保护，否则会无限递归创建子进程
> - 进程间不共享内存，因此每个子进程都有独立的 `is_prime` 函数副本

### 2.3 IO 密集型场景对比

**任务**：批量调用 100 个 HTTP API

#### Java 实现（线程池）

```java
ExecutorService executor = Executors.newFixedThreadPool(10);
List<String> urls = List.of(/* 100 个 URL */);

List<CompletableFuture<String>> futures = urls.stream()
    .map(url -> CompletableFuture.supplyAsync(() -> fetchUrl(url), executor))
    .toList();

List<String> results = futures.stream()
    .map(CompletableFuture::join)
    .toList();

executor.shutdown();
```

#### Python 实现 1（线程池 - 推荐简单场景）

```python
from concurrent.futures import ThreadPoolExecutor
import requests

urls = [...]  # 100 个 URL

def fetch_url(url):
    response = requests.get(url)
    return response.text

with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(fetch_url, urls))
# ✅ IO 密集型，线程池有效
```

#### Python 实现 2（异步协程 - 推荐高并发场景）

```python
import asyncio
import aiohttp

async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

asyncio.run(main())
# ✅ 协程开销更小，适合数千并发
```

**对比总结**：
- Java：`ExecutorService` 通用性强，适合 CPU/IO 场景
- Python：
  - IO 密集型优先 `asyncio`（轻量）
  - CPU 密集型必须用 `multiprocessing`

### 2.4 锁与同步

#### Java 实现（synchronized）

```java
class Counter {
    private int count = 0;

    public synchronized void increment() {
        count++;
    }

    public synchronized int getCount() {
        return count;
    }
}
```

#### Python 实现（threading.Lock）

```python
import threading

class Counter:
    def __init__(self):
        self.count = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:  # 上下文管理器自动加锁/解锁
            self.count += 1

    def get_count(self):
        with self.lock:
            return self.count
```

**关键差异**：
- Java 的 `synchronized` 是语言级关键字
- Python 需手动管理锁，但 `with` 语句保证异常安全

---

## 3. Web 框架对比

### 3.1 框架定位

| 框架 | 语言 | 定位 | 核心特性 |
|------|------|------|----------|
| **Spring Boot** | Java | 企业级全栈框架 | IoC/DI、AOP、自动配置、生态丰富 |
| **FastAPI** | Python | 现代高性能 API 框架 | 类型提示、自动文档、异步支持 |

### 3.2 最小可运行示例

#### Spring Boot（Java）

**pom.xml**：
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-validation</artifactId>
</dependency>
```

**HelloController.java**：
```java
@RestController
@RequestMapping("/api")
public class HelloController {

    // 依赖注入（构造器注入 - 推荐方式）
    private final UserService userService;

    @Autowired
    public HelloController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("/hello")
    public Map<String, String> hello(@RequestParam String name) {
        return Map.of("message", "Hello, " + name);
    }

    @PostMapping("/users")
    public User createUser(@RequestBody @Valid User user) {
        // 自动校验 @NotNull、@Email 等注解
        return userService.save(user);
    }
}
```

> **依赖注入说明**：详细的依赖注入对比请参考 [3.4 节](#34-依赖注入对比)

#### FastAPI（Python）

**main.py**：
```python
from fastapi import FastAPI, Query
from pydantic import BaseModel, EmailStr

app = FastAPI()

@app.get("/api/hello")
async def hello(name: str = Query(...)):  # 等价于 @RequestParam
    return {"message": f"Hello, {name}"}

class User(BaseModel):
    name: str
    email: EmailStr  # 自动校验邮箱格式

@app.post("/api/users")
async def create_user(user: User):  # 等价于 @RequestBody
    # Pydantic 自动校验类型
    return user
```

**运行**：
```bash
uvicorn main:app --reload
```

**自动文档**：访问 `http://localhost:8000/docs` 即可看到 Swagger UI

### 3.3 功能对照表

| 功能 | Spring Boot | FastAPI |
|------|-------------|---------|
| **路由定义** | `@GetMapping("/path")` | `@app.get("/path")` |
| **路径参数** | `@PathVariable` | 函数参数 + 类型提示 |
| **查询参数** | `@RequestParam` | `Query(...)` |
| **请求体** | `@RequestBody` | Pydantic 模型 |
| **参数校验** | JSR-303 注解（`@Valid`, `@NotNull`） | Pydantic 字段校验 |
| **依赖注入** | `@Autowired` / 构造器注入 | `Depends()` |
| **异常处理** | `@ExceptionHandler` | `@app.exception_handler()` |
| **中间件** | `Filter` / `Interceptor` | `@app.middleware()` |
| **异步支持** | `@Async` / WebFlux | 原生 `async/await` |

### 3.4 依赖注入对比

#### Spring Boot

```java
@Service
public class UserService {
    private final UserRepository repository;

    @Autowired  // 构造器注入（推荐）
    public UserService(UserRepository repository) {
        this.repository = repository;
    }
}

@RestController
public class UserController {
    private final UserService userService;

    @Autowired
    public UserController(UserService userService) {
        this.userService = userService;
    }
}
```

#### FastAPI

```python
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    # db 由 Depends 自动注入
    return db.query(User).filter(User.id == user_id).first()
```

**关键差异**：
- Spring Boot 基于类（`@Autowired` 注入）
- FastAPI 基于函数（`Depends()` 声明依赖）

### 3.5 异常处理

#### Spring Boot

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(ResourceNotFoundException ex) {
        return ResponseEntity.status(404)
            .body(new ErrorResponse(ex.getMessage()));
    }
}
```

#### FastAPI

```python
from fastapi import HTTPException
from fastapi.responses import JSONResponse

class ResourceNotFound(Exception):
    pass

@app.exception_handler(ResourceNotFound)
async def resource_not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": str(exc)}
    )

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    # db 通过 Depends 依赖注入（复用 3.4 节中的 get_db）
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ResourceNotFound(f"User {user_id} not found")
    return user
```

> **注意**：此示例复用了 3.4 节中定义的 `get_db` 依赖函数

---

## 4. 快速参考表

### 4.1 正则表达式速查

| 操作 | Java | Python |
|------|------|--------|
| 编译正则 | `Pattern.compile("\\d+")` | `re.compile(r"\d+")` |
| 全文匹配 | `matcher.matches()` | `re.fullmatch()` |
| 查找第一个 | `matcher.find()` | `re.search()` |
| 查找所有 | `matcher.find()` 循环 | `re.findall()` |
| 替换 | `matcher.replaceAll()` | `re.sub()` |

### 4.2 并发模型选择决策树

```
任务类型？
├─ CPU 密集型（计算、加密）
│  ├─ Java → 多线程（ThreadPoolExecutor）
│  └─ Python → 多进程（multiprocessing）
│
└─ IO 密集型（网络、文件）
   ├─ Java → CompletableFuture / 线程池
   └─ Python
      ├─ 并发数 < 100 → ThreadPoolExecutor
      └─ 并发数 > 100 → asyncio
```

### 4.3 Web 框架功能映射

| Spring Boot 概念 | FastAPI 对应 |
|------------------|--------------|
| `@RestController` | `app = FastAPI()` |
| `@GetMapping` | `@app.get()` |
| `@RequestBody` | Pydantic 模型 |
| `@Autowired` | `Depends()` |
| `@Valid` | Pydantic 自动校验 |
| `@ExceptionHandler` | `@app.exception_handler()` |

---

## 📌 总结

### Java 开发者学习 Python 的关键心态转变

1. **正则**：习惯使用原始字符串 `r""`，减少转义困扰
2. **并发**：理解 GIL，CPU 密集型必须用多进程
3. **Web**：FastAPI 通过类型提示实现自动校验，无需 XML 配置
4. **生态**：Python 生态更轻量，但企业级完整性不如 Java

### 推荐学习路径

1. 从正则和基础并发开始，熟悉 Python 语法特性
2. 实践 `asyncio` 和 `multiprocessing`，理解 GIL 影响
3. 使用 FastAPI 构建小型 API，体验类型提示的便利
4. 阅读本项目的 `03.项目实战` 案例，深入微服务实战

---

**下一步**：
- [为各章节添加挑战任务](../01.Python语言基础/01_快速上手与基础语法.md#🎯-开放式挑战)
- [前端调试控制台使用指南](../frontend/README.md)
- [返回学习规划](./Python学习规划_Java开发者版.md)