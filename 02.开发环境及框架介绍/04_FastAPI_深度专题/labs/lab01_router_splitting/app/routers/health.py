from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/", summary="健康检查")
def health_check() -> dict:
    """无需任何依赖或权限，方便上游系统探活。"""
    return {"status": "ok"}
