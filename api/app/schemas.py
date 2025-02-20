from typing import Optional
from pydantic import BaseModel

class ProductSearchSchema(BaseModel):
    title: Optional[str] = None
    main_category: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    limit: Optional[int] = 100
