from fastapi import FastAPI
from databases import Database
import os

DATABASE_URI = os.getenv('DATABASE_URI')

database = Database(DATABASE_URI)

app = FastAPI(openapi_url="/api/categories/openapi.json", docs_url="/api/categories/docs")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
