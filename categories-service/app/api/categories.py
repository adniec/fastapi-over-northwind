from fastapi import APIRouter

from app.api import db
from app.api.models import CategoryIn, CategoryOut

categories = APIRouter()


@categories.get('/all')
async def get_all():
    """Return all categories stored in database."""
    all_categories = await db.get_categories()
    return {'Categories': all_categories}


@categories.post('/new', response_model=CategoryOut, status_code=201)
async def create(payload: CategoryIn):
    category_id = await db.add_category(payload)

    response = {
        'category_id': category_id,
        **payload.dict()
    }

    return response


@categories.delete('/del/{category_id}')
async def delete(category_id: int):
    """Delete category with set id."""
    result = await db.delete(category_id)
    return {'Deleted': result}
