from sqlalchemy import Boolean, Column, Integer, String

from .database import Base


class Todo(Base):
    """待办事项 ORM 模型。"""

    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    completed = Column(Boolean, default=False, nullable=False)

