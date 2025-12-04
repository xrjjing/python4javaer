from fastapi import APIRouter, Depends, HTTPException, status

from app.deps import FakeDB, get_db

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", summary="列出所有示例商品")
def list_products(db: FakeDB = Depends(get_db)) -> list:
    """直接返回伪数据库中的商品列表。"""
    return db["products"]


@router.get("/{product_id}", summary="按 ID 查询商品")
def get_product(product_id: int, db: FakeDB = Depends(get_db)) -> dict:
    """
    演示如何在另一个 router 中复用同一依赖。
    通过不同领域的路由文件达到"单一职责"。
    """
    for product in db["products"]:
        if product["id"] == product_id:
            return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"product {product_id} not found",
    )
