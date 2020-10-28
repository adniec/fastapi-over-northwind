from pydantic import BaseModel
from typing import Optional


class CategoryIn(BaseModel):
    category_name: str
    description: str
    picture: bytes


class CategoryOut(CategoryIn):
    category_id: int


class CategoryUpdate(CategoryIn):
    category_name: Optional[str] = None
    description: Optional[str] = None
    picture: Optional[bytes] = None
