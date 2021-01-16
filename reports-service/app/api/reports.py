from fastapi import APIRouter
from prometheus_client import Summary

reports = APIRouter()

request_metrics = Summary('request_processing_seconds', 'Time spent processing request')
