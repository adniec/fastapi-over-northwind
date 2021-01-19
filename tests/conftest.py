import pytest
import requests


@pytest.fixture()
def url():
    return 'http://0.0.0.0:8080/api'


@pytest.fixture()
def auth():
    return {'headers': {'Authorization': 'Bearer Basic YWRtaW46cGFzc3dvcmQ='}}


@pytest.fixture()
def call(url):
    def response(method, endpoint, **kwargs):
        return requests.request(method, url + endpoint, **kwargs)

    return response
