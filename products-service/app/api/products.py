from fastapi import APIRouter, Depends, HTTPException

from app.api import db
from app.api.auth import authorize
from app.api.models import Product

products = APIRouter()


@products.post('/search')
async def search(payload: Product):
    parameters = {k: v for k, v in payload.dict().items() if v is not None}
    return await db.search(parameters)
