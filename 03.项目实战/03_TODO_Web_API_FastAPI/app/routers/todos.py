from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("/", response_model=List[schemas.TodoOut])
def list_todos(db: Session = Depends(get_db)):
    """查询全部 TODO。"""
    return db.query(models.Todo).all()


@router.post(
    "/", response_model=schemas.TodoOut, status_code=status.HTTP_201_CREATED
)
def create_todo(todo_in: schemas.TodoCreate, db: Session = Depends(get_db)):
    """创建新的 TODO。"""
    todo = models.Todo(title=todo_in.title, completed=todo_in.completed)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@router.put("/{todo_id}", response_model=schemas.TodoOut)
def update_todo(
    todo_id: int, todo_in: schemas.TodoUpdate, db: Session = Depends(get_db)
):
    """根据 ID 更新 TODO，支持局部更新。"""
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo 不存在")

    if todo_in.title is not None:
        todo.title = todo_in.title
    if todo_in.completed is not None:
        todo.completed = todo_in.completed

    db.commit()
    db.refresh(todo)
    return todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """根据 ID 删除 TODO。"""
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo 不存在")

    db.delete(todo)
    db.commit()
    return None

