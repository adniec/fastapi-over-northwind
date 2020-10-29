from fastapi import APIRouter, HTTPException
from typing import List

from app.api import db
from app.api.models import CategoryIn, CategoryOut, CategoryUpdate

categories = APIRouter()


@categories.get('/all', response_model=List[CategoryOut])
async def get_all():
    """Return all categories stored in database."""
    return await db.get_categories()


@categories.get('/{category_id}', response_model=CategoryOut)
async def get_by_id(category_id: int):
    """Return category with set id."""
    category = await db.get_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found.")
    return category


@categories.post('/new', response_model=CategoryOut, status_code=201)
async def create(payload: CategoryIn):
    """Create new category from send data."""
    category_id = await db.add_category(payload)
    return CategoryOut(**payload.dict(), category_id=category_id)


@categories.put('/update/{category_id}', response_model=CategoryOut)
async def update(category_id: int, payload: CategoryUpdate):
    """Update category with set id by sent payload."""
    category = await get_by_id(category_id)

    data = CategoryIn(**category)
    new_data = payload.dict(exclude_unset=True)
    merged = data.copy(update=new_data)

    if category_id == await db.update(category_id, merged):
        return CategoryOut(**merged.dict(), category_id=category_id)


@categories.delete('/del/{category_id}', response_model=CategoryOut)
async def delete(category_id: int):
    """Delete category with set id."""
    category = await get_by_id(category_id)

    if category_id == await db.delete(category_id):
        return category
