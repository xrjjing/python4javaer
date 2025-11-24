from pydantic import BaseModel


class TodoBase(BaseModel):
    """TODO 基础字段。"""

    title: str
    completed: bool = False


class TodoCreate(TodoBase):
    """创建 TODO 时使用的请求体。"""

    pass


class TodoUpdate(BaseModel):
    """更新 TODO 时使用的请求体，字段均为可选。"""

    title: str | None = None
    completed: bool | None = None


class TodoOut(TodoBase):
    """返回给客户端的 TODO 数据模型。"""

    id: int

    class Config:
        orm_mode = True

