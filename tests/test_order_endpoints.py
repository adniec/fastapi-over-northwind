from json import dumps

import pytest

from .sample_data import order


@pytest.mark.paypal
@pytest.mark.parametrize('payload', (order.correct(), order.correct_without_optional()))
def test_order_correct_make(call, auth, payload):
    response = call('POST', '/orders/make', **auth, data=dumps(payload))
    assert 'https://www.sandbox.paypal.com/checkoutnow' in response.json()
    assert response.status_code == 201


@pytest.mark.parametrize('payload,target', (
        (order.with_wrong_customer_id(), 'Customer'),
        (order.with_wrong_shipper_id(), 'Shipper'),
))
def test_order_make_with_wrong_id(call, auth, payload, target):
    response = call('POST', '/orders/make', **auth, data=dumps(payload))
    assert response.json().get('detail') == f'{target} with set id not found.'
    assert response.status_code == 404


@pytest.mark.parametrize('payload', (
        order.with_wrong_date(),
        order.without_product_id(),
        order.without_product_quantity(),
        order.with_too_high_product_quantity(),
        *order.populate_with_missing_field(),
))
def test_order_make_with_wrong_data(call, auth, payload):
    response = call('POST', '/orders/make', **auth, data=dumps(payload))
    assert response.status_code == 422


def test_send_order_with_wrong_status(call, auth):
    response = call('GET', '/orders/send/10248/1', **auth)
    assert response.json().get('detail') == 'Order cannot be send. Status not PAID.'
    assert response.status_code == 422
