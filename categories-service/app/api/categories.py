from fastapi import APIRouter, HTTPException

from app.api import db
from app.api.models import CategoryIn, CategoryOut, CategoryUpdate

categories = APIRouter()


@categories.get('/all')
async def get_all():
    """Return all categories stored in database."""
    all_categories = await db.get_categories()
    return {'Categories': all_categories}


@categories.get('/{category_id}', response_model=CategoryOut)
async def get_by_id(category_id: int):
    """Return category with set id."""
    category = await db.get_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found.")
    return category


@categories.post('/new', response_model=CategoryOut, status_code=201)
async def create(payload: CategoryIn):
    category_id = await db.add_category(payload)

    response = {
        'category_id': category_id,
        **payload.dict()
    }

    return response


@categories.put('/update/{category_id}', response_model=CategoryOut)
async def update(category_id: int, payload: CategoryUpdate):
    category = await get_by_id(category_id)

    data = CategoryIn(**category)
    new_data = payload.dict(exclude_unset=True)
    merged = data.copy(update=new_data)

    if category_id == await db.update(category_id, merged):
        return CategoryOut(**merged.dict(), category_id=category_id)


@categories.delete('/del/{category_id}')
async def delete(category_id: int):
    """Delete category with set id."""
    result = await db.delete(category_id)
    return {'Deleted': result}
