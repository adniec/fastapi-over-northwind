from json import dumps

import pytest

from .sample_data import category


@pytest.fixture(scope='module')
def ids():
    return []


@pytest.mark.dependency
@pytest.mark.run(order=4)
def test_category_correct_create(call, auth, ids):
    payload = category.new()
    response = call('POST', '/categories/new', **auth, data=dumps(payload))
    result = response.json()
    ids.append(result.get('category_id'))
    assert payload.items() <= result.items()
    assert response.status_code == 201


@pytest.mark.parametrize('payload', category.populate_with_missing_field())
def test_category_create_with_missing_field(call, auth, payload):
    response = call('POST', '/categories/new', **auth, data=dumps(payload))
    assert response.status_code == 422


@pytest.mark.dependency(depends=['test_category_correct_create'])
@pytest.mark.run(order=5)
@pytest.mark.parametrize('key,value', category.new().items())
def test_category_correct_update(call, auth, ids, key, value):
    payload = {'category_id': ids[0], key: value}
    response = call('PUT', '/categories/update', **auth, data=dumps(payload))
    assert payload.items() <= response.json().items()
    assert response.status_code == 200


@pytest.mark.parametrize('value,code', (
        (0, 404),
        ('abc', 422),
))
def test_category_update_with_wrong_id(call, auth, value, code):
    payload = category.from_db()
    payload['category_id'] = value
    response = call('PUT', '/categories/update', **auth, data=dumps(payload))
    assert response.status_code == code


@pytest.mark.dependency(depends=['test_category_correct_create'])
@pytest.mark.run(order=6)
def test_category_correct_delete(call, auth, ids):
    response = call('DELETE', f'/categories/del/{ids[0]}', **auth)
    assert isinstance(response.json(), dict)
    assert response.status_code == 200


def test_category_delete_not_existing(call, auth):
    response = call('DELETE', '/categories/del/0', **auth)
    assert response.json().get('detail') == 'Category not found.'
    assert response.status_code == 404


def test_category_delete_wrong_id_type(call, auth):
    response = call('DELETE', '/categories/del/abc', **auth)
    assert response.status_code == 422
