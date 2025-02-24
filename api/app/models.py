from sqlalchemy import Column, Integer, String
from .db import Base
from sqlmodel import SQLModel, Field
from typing import Optional
from decimal import Decimal
from sqlalchemy.dialects.postgresql import JSONB

# Remove thumb from Product model
class Product(SQLModel, table=True):
    __tablename__ = "products"

    parent_asin: str = Field(primary_key=True)
    main_category: Optional[str] = Field(default=None)
    title: Optional[str] = Field(default=None)
    average_rating: Optional[Decimal] = Field(default=None)
    rating_number: Optional[int] = Field(default=None)
    features: Optional[dict] = Field(default=None, sa_type=JSONB)
    description: Optional[dict] = Field(default=None, sa_type=JSONB)
    price: Optional[Decimal] = Field(default=None)
    store: Optional[str] = Field(default=None)
    categories: Optional[dict] = Field(default=None, sa_type=JSONB)
    details: Optional[dict] = Field(default=None, sa_type=JSONB)

class ProductImage(SQLModel, table=True):
    __tablename__ = "product_images"

    parent_asin: str = Field(foreign_key="products.parent_asin", primary_key=True)
    variant: str = Field(primary_key=True)
    large: str