from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Table

from app.api import metadata

products = Table(
    'products',
    metadata,
    Column('product_id', Integer, primary_key=True),
    Column('product_name', String),
    Column('supplier_id', Integer),
    Column('category_id', Integer),
    Column('quantity_per_unit', String),
    Column('unit_price', Integer),
    Column('units_in_stock', Integer),
    Column('units_on_order', Integer),
    Column('reorder_level', Integer),
    Column('discontinued', Integer),
)


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
