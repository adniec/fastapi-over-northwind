from fastapi import APIRouter, Depends, HTTPException

from app.api.auth import authorize

orders = APIRouter()
