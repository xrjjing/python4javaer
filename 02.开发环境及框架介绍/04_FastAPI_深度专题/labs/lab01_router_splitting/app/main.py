from fastapi import FastAPI

from app.routers import health, products, users

app = FastAPI(
    title="Lab01 Router Splitting",
    description="演示如何将 FastAPI 单体接口拆分成多个 APIRouter。",
)


# ⚠️ include_router 的顺序无强制要求，这里先注册公共路由
app.include_router(health.router)
app.include_router(users.router)
app.include_router(products.router)


@app.get("/")
def read_root() -> dict:
    """提供一个简单入口，可引导学习者查看文档页面。"""
    return {"message": "open /docs to explore routers"}
