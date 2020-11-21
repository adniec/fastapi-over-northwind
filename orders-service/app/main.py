from fastapi import FastAPI

from app.api.orders import orders
from app.api.db import database, engine, metadata

metadata.create_all(engine)

app = FastAPI(openapi_url="/api/orders/openapi.json", docs_url="/api/orders/docs")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(orders, prefix='/api/orders', tags=['orders'])
