from fastapi import APIRouter
from prometheus_client import Summary

from app.api import db
from app.api.auth import authorize
from app.api.models import Product

products = APIRouter()

request_metrics = Summary('request_processing_seconds', 'Time spent processing request')


@request_metrics.time()
@products.post('/search')
async def search(payload: Product):
    parameters = {k: v for k, v in payload.dict().items() if v is not None}
    return await db.search(parameters)
