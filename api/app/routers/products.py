from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import List

from ..db import get_db
from ..models import Product
from ..schemas import ProductSearchSchema

router = APIRouter()

@router.get("/products/search", response_model=List[Product])
async def search_products(
    search_params: ProductSearchSchema = Depends(), 
    db: AsyncSession = Depends(get_db)
):
    query = select(Product)

    if search_params.title:
        query = query.where(Product.title.ilike(f"%{search_params.title}%"))
    if search_params.main_category:
        query = query.where(Product.main_category == search_params.main_category)
    if search_params.min_price is not None:
        query = query.where(Product.price >= search_params.min_price)
    if search_params.max_price is not None:
        query = query.where(Product.price <= search_params.max_price)

    if search_params.limit is not None:
        if search_params.limit > 100:
                search_params.limit = 100
        query = query.limit(search_params.limit)

    result = await db.execute(query)
    return result.scalars().all()

@router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str, db: AsyncSession = Depends(get_db)):
    query = select(Product).where(Product.parent_asin == product_id)
    result = await db.execute(query)
    product = result.scalar_one_or_none()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
