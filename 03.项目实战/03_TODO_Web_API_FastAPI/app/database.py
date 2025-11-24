from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 使用当前目录下的 SQLite 数据库文件
SQLALCHEMY_DATABASE_URL = "sqlite:///./todo.db"

# 对于 SQLite，需要额外传入 check_same_thread 参数
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    FastAPI 依赖注入使用的数据库会话生成器。

    在路由函数中使用：
    db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

