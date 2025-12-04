# 03 数据模型与校验：Pydantic v2（FastAPI vs Java 视角）

> 面向对象：从 Java / Spring Boot 迁移到 Python / FastAPI 的同学。
> 目标：掌握 Pydantic v2 的数据模型定义、字段约束、自定义校验、配置管理与序列化，理解与 Java Bean Validation / Jackson 的映射关系。

---

## 0. 快速对照：Bean Validation vs Pydantic

| 维度 | Java (Bean Validation / Jackson) | Pydantic v2 |
| --- | --- | --- |
| 注解/字段 | `@NotNull/@Size/@Pattern/@Email` | `Field(min_length, max_length, pattern)`、`EmailStr` |
| 范围约束 | `@Min/@Max` | `Field(ge, le, gt, lt)` |
| 自定义校验 | `@Valid` + `ConstraintValidator` | `@field_validator` / `@model_validator` |
| 配置加载 | `@ConfigurationProperties` | `BaseSettings`（pydantic-settings） |
| 序列化控制 | `@JsonProperty/@JsonAlias` | `Field(alias, serialization_alias)` |
| ORM 转换 | Jackson getter 反射 | `model_config = {"from_attributes": True}` |
| 多态类型 | `@JsonTypeInfo/@JsonSubTypes` | `Annotated[Union[...], Field(discriminator)]` |

**记忆句**：Pydantic = Python 的"声明式校验 + Jackson 序列化"，无需 XML/注解扫描，模型即配置。

---

## 1. 基础模型与字段约束

### 1.1 最小示例

```python
from pydantic import BaseModel, Field, EmailStr

class UserSignup(BaseModel):
    # 对应 Java: @Size(min=3,max=20) @Pattern(regexp="...")
    username: str = Field(..., min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_]+$")
    # 对应 Java: @Min(18) @Max(120)
    age: int = Field(..., ge=18, le=120)
    # 对应 Java: @Email
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=64)

    model_config = {
        "str_strip_whitespace": True,  # 自动 trim，类似 Java 的预处理
    }
```

### 1.2 常用约束参数

| 参数 | 说明 | Java 对应 |
| --- | --- | --- |
| `min_length` / `max_length` | 字符串长度 | `@Size(min, max)` |
| `ge` / `le` / `gt` / `lt` | 数值范围（>=, <=, >, <） | `@Min` / `@Max` |
| `pattern` | 正则匹配 | `@Pattern` |
| `default` / `default_factory` | 默认值 | 字段初始化 |
| `...`（Ellipsis） | 必填字段 | `@NotNull` |

### 1.3 内建类型

Pydantic 提供开箱即用的类型：

```python
from pydantic import BaseModel, EmailStr, AnyUrl, IPvAnyAddress, SecretStr

class AppConfig(BaseModel):
    admin_email: EmailStr
    callback_url: AnyUrl
    server_ip: IPvAnyAddress
    api_key: SecretStr  # 打印时自动掩码

# 使用示例
config = AppConfig(
    admin_email="admin@example.com",
    callback_url="https://api.example.com/webhook",
    server_ip="192.168.1.1",
    api_key="secret-key-123"
)
print(config.api_key)  # SecretStr('**********')
```

---

## 2. 自定义校验器

### 2.1 字段级校验 @field_validator

```python
from pydantic import BaseModel, field_validator

class PasswordPair(BaseModel):
    password: str
    confirm: str

    @field_validator("password", mode="before")
    def strip_password(cls, v):
        """mode="before" 在类型转换前执行，类似 Java @PrePersist"""
        return v.strip() if isinstance(v, str) else v

    @field_validator("password", mode="after")
    def must_contain_digit(cls, v):
        """mode="after" 在类型转换后执行"""
        if not any(ch.isdigit() for ch in v):
            raise ValueError("密码需包含数字")
        return v
```

### 2.2 模型级校验 @model_validator

用于跨字段校验，类似 Java 的 `@AssertTrue` 或自定义 `ConstraintValidator`：

```python
from pydantic import model_validator

class PasswordPair(BaseModel):
    password: str
    confirm: str

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm:
            raise ValueError("两次密码不一致")
        return self
```

### 2.3 校验器执行顺序

```
输入数据
  ↓
field_validator(mode="before") → 类型转换 → field_validator(mode="after")
  ↓
model_validator(mode="after")
  ↓
最终模型实例
```

---

## 3. 嵌套模型与组合

### 3.1 嵌套对象

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class Address(BaseModel):
    city: str
    zipcode: str = Field(..., pattern=r"^\d{5,6}$")

class Profile(BaseModel):
    nickname: str
    tags: List[str] = Field(default_factory=list)
    extra: Dict[str, str] = Field(default_factory=dict)
    address: Address  # 嵌套模型自动递归校验
    backup_address: Optional[Address] = None
```

### 3.2 Java 对比

| 场景 | Java | Pydantic |
| --- | --- | --- |
| 嵌套校验 | `@Valid` 注解触发 | 自动递归，无需额外注解 |
| 集合校验 | `List<@Valid Item>` | `List[Item]` 自动校验每个元素 |
| 可选字段 | `@Nullable` + null 检查 | `Optional[T] = None` |

---

## 4. 判别联合类型（Discriminated Union）

多态请求体场景，类似 Java 的 `@JsonTypeInfo`：

```python
from typing import Annotated, Literal, Union
from pydantic import BaseModel, Field

class CardPayment(BaseModel):
    type: Literal["card"]
    card_no: str = Field(..., pattern=r"^\d{16}$")
    holder: str

class WalletPayment(BaseModel):
    type: Literal["wallet"]
    provider: Literal["apple", "google", "alipay", "wechat"]
    account: str

# 声明 discriminator，FastAPI 自动识别子类型
PaymentRequest = Annotated[
    Union[CardPayment, WalletPayment],
    Field(discriminator="type")
]
```

**FastAPI 路由使用（与上面模型放同一文件）：**

```python
from fastapi import FastAPI

app = FastAPI()

# CardPayment, WalletPayment, PaymentRequest 定义见上方

@app.post("/pay")
def pay(req: PaymentRequest):
    if isinstance(req, CardPayment):
        return {"method": "card", "card": req.card_no[-4:]}
    return {"method": "wallet", "provider": req.provider}
```

**测试示例：**

```python
# test_payment.py
import pytest
from pydantic import ValidationError

def test_card_payment():
    data = {"type": "card", "card_no": "1234567890123456", "holder": "Alice"}
    payment = PaymentRequest.model_validate(data)
    assert isinstance(payment, CardPayment)

def test_missing_discriminator():
    with pytest.raises(ValidationError):
        PaymentRequest.model_validate({"card_no": "1234567890123456"})
```

---

## 5. 模型转换与序列化

### 5.1 核心方法

| 方法 | 说明 | Java 对比 |
| --- | --- | --- |
| `model_validate(obj)` | 从 dict/对象创建模型 | `ObjectMapper.readValue()` |
| `model_dump()` | 转为 dict | `ObjectMapper.convertValue(obj, Map.class)` |
| `model_dump_json()` | 直接输出 JSON 字符串 | `ObjectMapper.writeValueAsString()` |

### 5.2 别名详解

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    id: int
    # alias: 仅影响输入（JSON→模型）
    # serialization_alias: 仅影响输出（模型→JSON）
    # 同时设置实现双向别名
    full_name: str = Field(
        alias="fullName",              # 输入时接受 fullName
        serialization_alias="fullName" # 输出时使用 fullName
    )
    email: str

    model_config = {
        "populate_by_name": True,  # 允许同时用字段名和别名
        "from_attributes": True    # 允许从 ORM 对象属性读取
    }

# 输入可以用别名
user1 = User.model_validate({"id": 1, "fullName": "Alice", "email": "a@example.com"})
# 也可以用字段名（因为 populate_by_name=True）
user2 = User(id=2, full_name="Bob", email="b@example.com")
print(user1.model_dump(by_alias=True))  # {"id": 1, "fullName": "Alice", ...}
```

### 5.3 ORM 对象转换

```python
class User(BaseModel):
    id: int
    full_name: str = Field(serialization_alias="fullName")
    email: str

    model_config = {
        "from_attributes": True  # 允许从 ORM 对象属性读取
    }

# ORM 对象（假设 SQLAlchemy 模型）
class UserORM:
    def __init__(self, id, full_name, email):
        self.id = id
        self.full_name = full_name
        self.email = email

# 转换
orm_obj = UserORM(1, "Alice Doe", "a@example.com")
user = User.model_validate(orm_obj)
print(user.model_dump(by_alias=True))  # {"id": 1, "fullName": "Alice Doe", ...}
```

### 5.3 常用 model_dump 参数

```python
user.model_dump(
    by_alias=True,      # 使用序列化别名
    exclude_none=True,  # 排除 None 值
    exclude={"password"},  # 排除敏感字段
    mode="json"         # JSON 兼容格式（datetime→str）
)
```

---

## 6. 配置与环境变量（BaseSettings）

### 6.1 安装

```bash
pip install pydantic-settings
```

> ⚠️ **v2 变更**：`BaseSettings` 已从 `pydantic` 拆分到 `pydantic-settings`。

### 6.2 基本用法

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="APP_",       # 环境变量前缀，类似 Spring prefix
        env_file=".env",         # 支持 .env 文件
        env_file_encoding="utf-8",
        case_sensitive=False,    # 环境变量大小写不敏感
    )

    debug: bool = False
    db_url: PostgresDsn
    redis_url: str = "redis://localhost:6379/0"
```

### 6.3 加载优先级

```
环境变量 > .env 文件 > 代码默认值
```

类似 Spring Boot 的 `application.yml` < 环境变量覆盖逻辑。

### 6.4 敏感信息处理

```python
from pydantic import SecretStr

class AppSettings(BaseSettings):
    api_key: SecretStr

settings = AppSettings()
print(settings.api_key)              # SecretStr('**********')
print(settings.api_key.get_secret_value())  # 真实值
```

---

## 7. 与 FastAPI 集成实践

### 7.1 请求/响应模型

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr

app = FastAPI()

class SignupReq(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(..., min_length=8)

class SignupResp(BaseModel):
    user_id: int
    username: str

@app.post("/signup", response_model=SignupResp)
def signup(req: SignupReq):
    # 校验自动完成，失败返回 422
    return SignupResp(user_id=1, username=req.username)
```

### 7.2 依赖注入中的模型复用

```python
from functools import lru_cache
from fastapi import Depends
from pydantic_settings import BaseSettings

class AppSettings(BaseSettings):
    debug: bool = False
    db_url: str = "sqlite:///./app.db"

@lru_cache  # 缓存避免每请求重建
def get_settings() -> AppSettings:
    return AppSettings()

@app.get("/config")
def show_config(settings: AppSettings = Depends(get_settings)):
    return {"debug": settings.debug}
```

### 7.3 全局异常格式

FastAPI 默认返回 422 格式：

```json
{
  "detail": [
    {
      "loc": ["body", "username"],
      "msg": "String should have at least 3 characters",
      "type": "string_too_short"
    }
  ]
}
```

---

## 8. ⚠️ 常见陷阱

### 8.1 v1 → v2 迁移问题

| 问题 | 原因 | 解决 |
| --- | --- | --- |
| `BaseSettings` 导入失败 | v2 拆包 | `from pydantic_settings import BaseSettings` |
| `Config` 类不生效 | v2 改为 `model_config` | 使用 dict 或 `ConfigDict` |
| `json_encoders` 位置变化 | v2 放入 `model_config` | `model_config = {"json_encoders": {...}}` |

### 8.2 Java 开发者常踩坑

1. **宽松解析**：`model_validate` 默认做类型转换（如 `"123"` → `123`），需严格时用 `strict=True`
   ```python
   from pydantic import BaseModel

   class Item(BaseModel):
       count: int

   # 宽松模式（默认）：字符串自动转 int
   Item.model_validate({"count": "123"})  # OK, count=123

   # 严格模式：类型必须精确匹配，类似 Java Bean Validation
   Item.model_validate({"count": "123"}, strict=True)  # ValidationError!
   ```
2. **别名混淆**：`alias` 仅影响输入，输出别名需用 `serialization_alias`
3. **联合类型无 discriminator**：导致解析失败或匹配到错误类型
4. **每请求创建 Settings**：性能问题，应用 `@lru_cache` 缓存

### 8.3 性能注意

```python
from functools import lru_cache

@lru_cache
def get_settings() -> AppSettings:
    return AppSettings()  # 只创建一次
```

---

## 9. 💡 最佳实践

1. **分层模型**：Request/Response/Domain/ORM 分开定义，避免耦合
2. **别名策略统一**：全局使用 `populate_by_name=True` 支持双向别名
3. **校验器单一职责**：每个 `@field_validator` 只做一件事
4. **配置集中管理**：所有配置走 `BaseSettings`，支持多环境
5. **敏感字段用 SecretStr**：防止日志泄露
6. **善用 `exclude` / `include`**：响应模型精确控制输出字段

---

## 10. 练习

### 练习 1：用户注册校验

创建 `UserCreate` 模型：
- `username`：3-20 字符，仅字母数字下划线
- `email`：有效邮箱
- `password` / `confirm_password`：8+ 字符，必须包含数字，两次输入一致

```python
# 提示：使用 @field_validator + @model_validator
```

### 练习 2：多态支付请求

实现 `PaymentRequest`（CardPayment / WalletPayment），在 FastAPI 路由中返回解析后的支付方式。

### 练习 3：配置加载

编写 `AppSettings`：
- 从 `.env` 读取 `APP_DB_URL`、`APP_REDIS_URL`
- 支持 `APP_DEBUG` 覆盖
- 敏感信息打掩码

### 练习 4：ORM 序列化

设计 `UserResponse` 模型：
- 输入字段蛇形（`full_name`）
- 输出驼峰（`fullName`）
- 从 ORM 对象实例化

---

## 11. Java vs Python 小贴士

| 场景 | Java 习惯 | Python/Pydantic 方式 |
| --- | --- | --- |
| 必填校验 | `@NotNull` | `Field(...)` 或不给默认值 |
| 分组校验 | `groups = {Create.class}` | 定义多个模型或条件校验器 |
| 级联校验 | `@Valid` | 自动递归，无需注解 |
| 自定义消息 | `message = "xxx"` | `raise ValueError("xxx")` |
| JSON 命名策略 | `@JsonNaming(SnakeCaseStrategy)` | `model_config = {"alias_generator": to_camel}` |
| 条件必填 | `@NotNull(condition)` | `@model_validator` 中编写逻辑 |

---

## 12. 小结

- Pydantic v2 是 FastAPI 的数据校验核心，声明式定义 + 自动校验
- `Field` 提供丰富的约束参数，对应 Java Bean Validation 注解
- `@field_validator` / `@model_validator` 实现自定义校验逻辑
- `BaseSettings` 统一管理配置，支持环境变量和 `.env`
- `model_dump` / `model_validate` 处理序列化与 ORM 转换
- 判别联合类型 (`discriminator`) 处理多态请求体
- 从 v1 迁移需注意 `pydantic-settings` 拆包和 `model_config` 变化
