from pydantic import BaseModel


class CategoryIn(BaseModel):
    category_name: str
    description: str
    picture: bytes


class CategoryOut(CategoryIn):
    category_id: int
