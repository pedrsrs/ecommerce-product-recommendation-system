from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlalchemy import and_
from typing import List

from ..db import get_db
from ..models import Product, ProductImage
from ..schemas import ProductSearchSchema, ProductRead

router = APIRouter()

@router.get("/products/search", response_model=List[ProductRead])
async def search_products(
    search_params: ProductSearchSchema = Depends(),
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),  
    limit: int = Query(50, le=100)  
):
    offset = (page - 1) * limit  

    query = (
        select(Product, ProductImage.large)
        .outerjoin(
            ProductImage,
            and_(
                Product.parent_asin == ProductImage.parent_asin,
                ProductImage.variant == "MAIN"
            )
        )
    )

    if search_params.title:
        query = query.where(Product.title.ilike(f"%{search_params.title}%"))
    if search_params.main_category:
        query = query.where(Product.main_category == search_params.main_category)
    if search_params.min_price is not None:
        query = query.where(Product.price >= search_params.min_price)
    if search_params.max_price is not None:
        query = query.where(Product.price <= search_params.max_price)

    query = query.limit(limit).offset(offset) 

    result = await db.execute(query)
    items = result.all()

    return [
        ProductRead(
            **product.dict(),
            image_large=image_large
        )
        for product, image_large in items
    ]

@router.get("/products/{product_id}", response_model=ProductRead)
async def get_product(product_id: str, db: AsyncSession = Depends(get_db)):
    query = (
        select(Product, ProductImage.large)
        .outerjoin(
            ProductImage,
            and_(
                Product.parent_asin == ProductImage.parent_asin,
                ProductImage.variant == "MAIN"
            )
        )
        .where(Product.parent_asin == product_id)
    )

    result = await db.execute(query)
    item = result.first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product, image_large = item
    return ProductRead(**product.dict(), image_large=image_large)