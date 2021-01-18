from fastapi import APIRouter
from prometheus_client import Summary
from typing import List

from app.api import db
from app.api.models import Date, Employee

reports = APIRouter()

request_metrics = Summary('request_processing_seconds', 'Time spent processing request')


@request_metrics.time()
@reports.post('/employees/activity', response_model=List[Employee])
async def get_employees_activity(payload: Date):
    """Return employees activity in set period of time."""
    return await db.get_employees_activity(**payload.dict())


@request_metrics.time()
@reports.post('/employees/delays', response_model=List[Employee])
async def get_employees_shipment_delays(payload: Date):
    """Return employees shipment delays in set period of time."""
    return await db.get_employees_shipment_delays(**payload.dict())
