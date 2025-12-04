"""FastAPI应用入口"""
from fastapi import FastAPI
from .config import settings
from .routers import log_detective

app = FastAPI(title=settings.SERVICE_NAME)

app.include_router(log_detective.router, prefix="/internal/log-detective")

@app.get("/health")
def health():
    return {"status": "ok"}
