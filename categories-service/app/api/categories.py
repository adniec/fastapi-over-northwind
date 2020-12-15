import base64
import imghdr
from typing import List

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from prometheus_client import Summary

from app.api import db
from app.api.auth import authorize
from app.api.models import CategoryIn, CategoryOut, CategoryUpdate

categories = APIRouter()

request_metrics = Summary('request_processing_seconds', 'Time spent processing request')


@request_metrics.time()
@categories.get('/all', response_model=List[CategoryOut])
async def get_all():
    """Return all categories stored in database."""
    return await db.get_categories()


@request_metrics.time()
@categories.get('/{category_id}', response_model=CategoryOut)
async def get_by_id(category_id: int):
    """Return category with set id."""
    category = await db.get_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail='Category not found.')
    return category


@request_metrics.time()
@categories.post('/new', response_model=CategoryOut, status_code=201, dependencies=[Depends(authorize)])
async def create(payload: CategoryIn):
    """Create new category from send data."""
    category_id = await db.add_category(payload)
    return CategoryOut(**payload.dict(), category_id=category_id)


@request_metrics.time()
@categories.post('/update/img/{category_id}', dependencies=[Depends(authorize)])
async def upload_file(category_id: int, file: UploadFile = File(...)):
    """Update category with set id by chosen image."""
    if not imghdr.what(file.file):
        raise HTTPException(status_code=415, detail='Wrong image format.')
    image = base64.encodebytes(file.file.read()).decode()
    return await update(CategoryUpdate(category_id=category_id, picture=image))


@request_metrics.time()
@categories.put('/update', response_model=CategoryOut, dependencies=[Depends(authorize)])
async def update(payload: CategoryUpdate):
    """Update category with set id by sent payload."""
    category = await get_by_id(payload.category_id)

    data = CategoryOut(**category)
    new_data = payload.dict(exclude_unset=True)
    merged = data.copy(update=new_data)

    if payload.category_id == await db.update(merged):
        return merged


@request_metrics.time()
@categories.delete('/del/{category_id}', response_model=CategoryOut, dependencies=[Depends(authorize)])
async def delete(category_id: int):
    """Delete category with set id."""
    category = await get_by_id(category_id)

    if category_id == await db.delete(category_id):
        return category
