from fastapi import APIRouter, Depends, HTTPException, status

from app.deps import FakeDB, get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", summary="列出所有示例用户")
def list_users(db: FakeDB = Depends(get_db)) -> list:
    """演示通过依赖注入获取共享数据。"""
    return db["users"]


@router.get("/{user_id}", summary="按 ID 查询用户")
def get_user(user_id: int, db: FakeDB = Depends(get_db)) -> dict:
    """
    通过最朴素的遍历在假数据中查找用户。
    真实项目里可替换为 ORM 查询或仓储层调用。
    """
    for user in db["users"]:
        if user["id"] == user_id:
            return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"user {user_id} not found",
    )
