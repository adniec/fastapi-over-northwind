import httpx
import os

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasicCredentials, HTTPBearer

orders = APIRouter()
security = HTTPBearer()


def authorize(credentials: HTTPBasicCredentials = Depends(security)):
    response = httpx.get(os.getenv('AUTH_SERVICE_URL'), headers={'Authorization': credentials.credentials})
    if response.status_code == 401:
        raise HTTPException(status_code=401)
