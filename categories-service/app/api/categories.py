from fastapi import APIRouter

from app.api import db
from app.api.models import CategoryIn, CategoryOut

categories = APIRouter()


@categories.post('/new', response_model=CategoryOut, status_code=201)
async def create(payload: CategoryIn):
    category_id = await db.add_category(payload)

    response = {
        'category_id': category_id,
        **payload.dict()
    }

    return response
