import os
import secrets

from databases import Database
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

DATABASE_URI = os.getenv('DATABASE_URI')

database = Database(DATABASE_URI)

app = FastAPI(openapi_url="/api/test/openapi.json", docs_url="/api/test/docs")

security = HTTPBasic()


def authorize(credentials: HTTPBasicCredentials = Depends(security)):
    is_user_ok = secrets.compare_digest(credentials.username, os.getenv('LOGIN'))
    is_pass_ok = secrets.compare_digest(credentials.password, os.getenv('PASSWORD'))

    if not (is_user_ok and is_pass_ok):
        raise HTTPException(
            status_code=401, headers={'WWW-Authenticate': 'Basic'})


@app.get('/api/test/get_states')
async def get_states():
    """Return all states stored in database."""
    return await database.fetch_all(query='SELECT * FROM us_states')


@app.get('/api/test/protected', dependencies=[Depends(authorize)])
async def protected():
    return {"Protected": True}


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
