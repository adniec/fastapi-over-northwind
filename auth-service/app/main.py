import os
import secrets

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.responses import Response

basic_security = HTTPBasic()

app = FastAPI(openapi_url=None)


def get_variable(name: str) -> str:
    path = os.getenv(name)
    with open(path, 'r') as f:
        return f.readline().rstrip('\n')


@app.get('/api/auth/basic', status_code=204, response_class=Response)
def auth(credentials: HTTPBasicCredentials = Depends(basic_security)):
    is_user_ok = secrets.compare_digest(credentials.username, get_variable('LOGIN'))
    is_pass_ok = secrets.compare_digest(credentials.password, get_variable('PASSWORD'))

    if not (is_user_ok and is_pass_ok):
        raise HTTPException(status_code=401, headers={'WWW-Authenticate': 'Basic'})
