from pydantic import BaseModel
from typing import Optional


class Product(BaseModel):
    product_id: Optional[int] = None
    product_name: Optional[str] = None
    supplier_id: Optional[int] = None
    category_id: Optional[int] = None
    quantity_per_unit: Optional[str] = None
    unit_price: Optional[int] = None
    units_in_stock: Optional[int] = None
    units_in_order: Optional[int] = None
    reorder_level: Optional[int] = None
    discontinued: Optional[int] = None
