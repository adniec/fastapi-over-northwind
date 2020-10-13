from fastapi import FastAPI
from databases import Database
import os

DATABASE_URI = os.getenv('DATABASE_URI')

database = Database(DATABASE_URI)

app = FastAPI(openapi_url="/api/test/openapi.json", docs_url="/api/test/docs")

@app.get('/api/test/get_states')
async def get_states():
    """Return all states stored in database."""
    return await database.fetch_all(query='SELECT * FROM us_states')

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
