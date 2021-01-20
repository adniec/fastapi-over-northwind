from json import dumps

import pytest

from .sample_data import date


@pytest.fixture(scope="module", params=[
    '/reports/customers/profit',
    '/reports/employees/activity',
    '/reports/employees/delays',
    '/reports/products/popularity',
])
def endpoint(request):
    return request.param


@pytest.mark.parametrize('payload', (
        date.correct(),
        date.correct_in_seconds(),
))
def test_correct_report(call, auth, endpoint, payload):
    response = call('POST', endpoint, **auth, data=dumps(payload))
    assert isinstance(response.json(), list)
    assert response.status_code == 200


@pytest.mark.parametrize('payload', (
        date.with_wrong_values(),
        date.with_higher_from_date(),
        *date.populate_with_missing_field(),
))
def test_report_with_wrong_dates(call, auth, endpoint, payload):
    response = call('POST', endpoint, **auth, data=dumps(payload))
    assert response.status_code == 422
