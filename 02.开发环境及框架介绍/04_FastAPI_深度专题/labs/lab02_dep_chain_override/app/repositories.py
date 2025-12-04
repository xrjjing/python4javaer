# app/repositories.py
"""
仓储层：封装数据访问逻辑
Java 对比：Spring Data Repository / DAO
"""
from sqlalchemy.orm import Session
from sqlalchemy import select

from .models import User


class UserRepository:
    """
    用户仓储
    Java 对比：public interface UserRepository extends JpaRepository<User, Long>
    """

    def __init__(self, session: Session):
        self.session = session

    def create(self, name: str, email: str) -> User:
        """创建用户"""
        user = User(name=name, email=email)
        self.session.add(user)
        self.session.flush()  # 立即获取自增 ID
        return user

    def get(self, user_id: int) -> User | None:
        """根据 ID 获取用户"""
        return self.session.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        """根据邮箱获取用户"""
        stmt = select(User).where(User.email == email)
        return self.session.execute(stmt).scalar_one_or_none()

    def list_all(self) -> list[User]:
        """获取所有用户"""
        stmt = select(User).order_by(User.id)
        return list(self.session.execute(stmt).scalars().all())

    def update(self, user_id: int, name: str = None, email: str = None) -> User | None:
        """更新用户"""
        user = self.get(user_id)
        if not user:
            return None
        if name:
            user.name = name
        if email:
            user.email = email
        self.session.flush()
        return user

    def delete(self, user_id: int) -> bool:
        """删除用户"""
        user = self.get(user_id)
        if not user:
            return False
        self.session.delete(user)
        return True
