import httpx
import os
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasicCredentials, HTTPBearer

from app.api import db
from app.api.models import Product

products = APIRouter()
security = HTTPBearer()


def authorize(credentials: HTTPBasicCredentials = Depends(security)):
    response = httpx.get(os.getenv('AUTH_SERVICE_URL'), headers={'Authorization': credentials.credentials})
    if response.status_code == 401:
        raise HTTPException(status_code=401)


@products.post('/search')
async def search(payload: Product):
    parameters = {k: v for k, v in payload.dict().items() if v is not None}
    return await db.search(parameters)
