from typing import Optional
from pydantic import BaseModel, field_validator
from sqlmodel import SQLModel, Field
from decimal import Decimal
from sqlalchemy.dialects.postgresql import JSONB

class ProductSearchSchema(BaseModel):
    title: Optional[str] = None
    main_category: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    limit: Optional[int] = 100
    page: Optional[int] = 1

class ProductRead(SQLModel):
    parent_asin: str
    main_category: Optional[str] = None
    title: Optional[str] = None
    average_rating: Optional[Decimal] = None
    rating_number: Optional[int] = None
    features: Optional[dict] = Field(default=None, sa_type=JSONB)
    description: Optional[dict] = Field(default=None, sa_type=JSONB)
    price: Optional[Decimal] = None
    store: Optional[str] = None
    categories: Optional[dict] = Field(default=None, sa_type=JSONB)
    details: Optional[dict] = None
    image_large: Optional[str] = None

    @field_validator('features', 'description', 'categories', mode='before')
    def convert_empty_list_to_dict(cls, value):
        return value if isinstance(value, dict) else {}
