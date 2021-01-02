from fastapi import APIRouter, Depends, HTTPException
from prometheus_client import Summary

from app.api.auth import authorize

orders = APIRouter()

request_metrics = Summary('request_processing_seconds', 'Time spent processing request')
