# app/routers/users.py
"""
用户路由：依赖链的终点
依赖链：Settings → Engine → Session → Repository → Route
Java 对比：@RestController
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr

from ..deps import get_user_repo
from ..repositories import UserRepository

router = APIRouter(prefix="/users", tags=["users"])


# === Pydantic 模型 ===
class UserCreate(BaseModel):
    """创建用户请求"""
    name: str
    email: EmailStr


class UserUpdate(BaseModel):
    """更新用户请求"""
    name: str | None = None
    email: EmailStr | None = None


class UserResponse(BaseModel):
    """用户响应"""
    id: int
    name: str
    email: str

    model_config = {"from_attributes": True}


# === 路由 ===
@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, repo: UserRepository = Depends(get_user_repo)):
    """
    创建用户
    Java 对比：@PostMapping + @RequestBody
    """
    # 检查邮箱是否已存在
    if repo.get_by_email(payload.email):
        raise HTTPException(status_code=400, detail="邮箱已被使用")
    return repo.create(payload.name, payload.email)


@router.get("", response_model=list[UserResponse])
def list_users(repo: UserRepository = Depends(get_user_repo)):
    """
    获取所有用户
    Java 对比：@GetMapping
    """
    return repo.list_all()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, repo: UserRepository = Depends(get_user_repo)):
    """
    根据 ID 获取用户
    Java 对比：@GetMapping("/{id}") + @PathVariable
    """
    user = repo.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, payload: UserUpdate, repo: UserRepository = Depends(get_user_repo)):
    """
    更新用户
    Java 对比：@PutMapping + @RequestBody
    """
    user = repo.update(user_id, name=payload.name, email=payload.email)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, repo: UserRepository = Depends(get_user_repo)):
    """
    删除用户
    Java 对比：@DeleteMapping
    """
    if not repo.delete(user_id):
        raise HTTPException(status_code=404, detail="用户不存在")
    return None
