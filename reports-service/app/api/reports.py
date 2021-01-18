from fastapi import APIRouter
from prometheus_client import Summary
from typing import List

from app.api import db
from app.api.models import Date, EmployeeReport

reports = APIRouter()

request_metrics = Summary('request_processing_seconds', 'Time spent processing request')


@request_metrics.time()
@reports.post('/employees/activity', response_model=List[EmployeeReport])
async def get_employees_activity(payload: Date):
    """Return employees activity in set period of time."""
    return await db.get_employees_report(**payload.dict())
