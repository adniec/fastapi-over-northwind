import pytest


@pytest.fixture()
def get(call, auth):
    def response(endpoint, is_auth):
        kwargs = auth if is_auth else {}
        return call('GET', endpoint, **kwargs)

    return response


@pytest.mark.parametrize('endpoint,instance,is_auth', (
        ('/categories/all', list, False),
        ('/categories/1', dict, False),
        ('/orders/all', list, True),
        ('/orders/details/11044', list, True),
        ('/orders/shippers', list, False),
        ('/products/1', dict, False),
        ('/reports/products/reorder', list, False),
))
def test_correct_get_response(get, endpoint, instance, is_auth):
    response = get(endpoint, is_auth)
    assert isinstance(response.json(), instance)
    assert response.status_code == 200


@pytest.mark.parametrize('endpoint,subject,is_auth', (
        ('/categories/1000', 'Category', False),
        ('/orders/details/1', 'Order', True),
        ('/products/1000', 'Product', False),
))
def test_not_found_get_response(get, endpoint, subject, is_auth):
    response = get(endpoint, is_auth)
    assert response.json().get('detail') == f'{subject} not found.'
    assert response.status_code == 404


@pytest.mark.parametrize('endpoint, is_auth', (
        ('/categories/abc', False),
        ('/orders/details/abc', True),
        ('/products/abc', False),
))
def test_wrong_value_get_responses(get, endpoint, is_auth):
    response = get(endpoint, is_auth)
    assert response.status_code == 422
