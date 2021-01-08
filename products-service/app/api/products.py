from typing import List

from fastapi import APIRouter, Depends, HTTPException
from prometheus_client import Summary

from app.api import db
from app.api.auth import authorize
from app.api.models import ProductIn, ProductOut, ProductUpdate, ProductSearch

products = APIRouter()

request_metrics = Summary('request_processing_seconds', 'Time spent processing request')


@request_metrics.time()
@products.get('/{product_id}', response_model=ProductOut)
async def get_by_id(product_id: int):
    """Return product with set id."""
    product = await db.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail='Product not found.')
    return product


@request_metrics.time()
@products.post('/search', response_model=List[ProductOut])
async def search(payload: ProductSearch):
    """Return products matching payload."""
    parameters = {k: v for k, v in payload.dict().items() if v is not None}
    return await db.search(parameters)


@request_metrics.time()
@products.post('/new', response_model=ProductOut, status_code=201, dependencies=[Depends(authorize)])
async def create(payload: ProductIn):
    """Create new product from sent data."""
    product_id = await db.add_product(payload)
    return ProductOut(**payload.dict(), product_id=product_id)


@request_metrics.time()
@products.put('/update', response_model=ProductOut, dependencies=[Depends(authorize)])
async def update(payload: ProductUpdate):
    """Update product with set id by sent payload."""
    product = await get_by_id(payload.product_id)

    data = ProductOut(**product)
    new_data = payload.dict(exclude_unset=True)
    merged = data.copy(update=new_data)

    if payload.product_id == await db.update(merged):
        return merged


@request_metrics.time()
@products.delete('/del/{product_id}', response_model=ProductOut, dependencies=[Depends(authorize)])
async def delete(product_id: int):
    """Delete product with set id."""
    product = await get_by_id(product_id)

    if product_id == await db.delete(product_id):
        return product
