import pytest


@pytest.mark.parametrize('endpoint,method', (
        ('/categories/new', 'POST'),
        ('/categories/update/img/1', 'POST'),
        ('/categories/update', 'PUT'),
        ('/categories/del/1', 'DELETE'),
        ('/orders/all', 'GET'),
        ('/orders/details/1', 'GET'),
        ('/orders/make', 'POST'),
        ('/orders/send/1/1', 'GET'),
        ('/products/new', 'POST'),
        ('/products/update', 'PUT'),
        ('/products/del/1', 'DELETE'),
        ('/reports/customers/profit', 'POST'),
        ('/reports/employees/activity', 'POST'),
        ('/reports/employees/delays', 'POST'),
        ('/reports/products/popularity', 'POST'),
        ('/reports/products/reorder', 'GET'),
))
def test_unauthorized_access(call, endpoint, method):
    response = call(method, endpoint)
    assert response.status_code == 403
