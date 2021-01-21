from json import dumps

import pytest

from .sample_data import product


@pytest.fixture(scope='module')
def ids():
    return []


@pytest.mark.parametrize('key,value', product.from_db().items())
def test_product_in_db_search_by_each_field(call, key, value):
    response = call('POST', '/products/search', data=dumps({key: value}))
    result = response.json()
    assert response.status_code == 200
    assert isinstance(result, list)
    assert len(result) > 0


def test_product_in_db_search_by_all_fields(call):
    response = call('POST', '/products/search', data=dumps(product.from_db()))
    result = response.json()
    assert response.status_code == 200
    assert result == [product.from_db()]


def test_product_not_in_db_search(call):
    data = {
        'product_name': 'abc',
        'units_in_stock': 5000
    }
    response = call('POST', '/products/search', data=dumps(data))
    result = response.json()
    assert response.status_code == 200
    assert isinstance(result, list)
    assert len(result) == 0


@pytest.mark.parametrize('data', ({}, {'not_a_product_name': 'abc', 'units_in_no_stock': 50}))
def test_all_product_search_with_ignored_fields(call, data):
    response = call('POST', '/products/search', data=dumps(data))
    assert isinstance(response.json(), list)
    assert response.status_code == 200


@pytest.mark.parametrize('key,value', product.with_wrong_types().items())
def test_product_search_by_each_wrong_type_field(call, key, value):
    response = call('POST', '/products/search', data=dumps({key: value}))
    assert response.status_code == 422


@pytest.mark.dependency
@pytest.mark.run(order=1)
def test_product_correct_create(call, auth, ids):
    payload = product.new()
    response = call('POST', '/products/new', **auth, data=dumps(payload))
    result = response.json()
    ids.append(result.get('product_id'))
    assert payload.items() <= result.items()
    assert response.status_code == 201


@pytest.mark.parametrize('payload', (
        *product.populate_with_missing_field(),
        *product.populate_with_wrong_field(),
))
def test_product_create_with_wrong_field_value(call, auth, payload):
    response = call('POST', '/products/new', **auth, data=dumps(payload))
    assert response.status_code == 422


@pytest.mark.parametrize('key', ('supplier_id', 'category_id'))
def test_product_create_with_wrong_foreign_key(call, auth, key):
    payload = product.new()
    payload[key] = 0
    response = call('POST', '/products/new', **auth, data=dumps(payload))
    assert response.json().get('detail') == 'Wrong foreign key. Record with set id not in database.'
    assert response.status_code == 422


@pytest.mark.dependency(depends=['test_product_correct_create'])
@pytest.mark.run(order=2)
@pytest.mark.parametrize('key,value', product.new().items())
def test_product_correct_update(call, auth, ids, key, value):
    payload = {'product_id': ids[0], key: value}
    response = call('PUT', '/products/update', **auth, data=dumps(payload))
    assert payload.items() <= response.json().items()
    assert response.status_code == 200


@pytest.mark.parametrize('payload', (
        *product.populate_with_wrong_field(),
))
def test_product_update_with_wrong_field_value(call, auth, payload):
    payload['product_id'] = 1
    response = call('PUT', '/products/update', **auth, data=dumps(payload))
    assert response.status_code == 422


@pytest.mark.dependency(depends=['test_product_correct_create'])
@pytest.mark.run(order=3)
def test_product_correct_delete(call, auth, ids):
    response = call('DELETE', f'/products/del/{ids[0]}', **auth)
    assert isinstance(response.json(), dict)
    assert response.status_code == 200


def test_product_delete_not_existing(call, auth):
    response = call('DELETE', '/products/del/0', **auth)
    assert response.json().get('detail') == 'Product not found.'
    assert response.status_code == 404


def test_product_delete_wrong_id_type(call, auth):
    response = call('DELETE', '/products/del/abc', **auth)
    assert response.status_code == 422
