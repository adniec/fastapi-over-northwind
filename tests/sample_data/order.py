from datetime import date


def correct():
    return {
        'customer_id': 'ALFKI',
        'required_date': '2025-01-01',
        'ship_via': 1,
        'address': {
            'company_name': 'Test Inc.',
            'address': 'Test st. 123',
            'city': 'Test',
            'region': 'Test',
            'postal_code': '12345',
            'country': 'Test'
        },
        'products': [
            {
                'product_id': 2,
                'quantity': 1
            },
            {
                'product_id': 9,
                'quantity': 2
            }
        ]
    }


def correct_without_optional():
    order = correct()
    order.pop('required_date')
    order.pop('address')
    return order


def with_wrong_customer_id():
    order = correct()
    order['customer_id'] = 'Test'
    return order


def with_wrong_shipper_id():
    order = correct()
    order['ship_via'] = 0
    return order


def with_wrong_date():
    order = correct()
    order['required_date'] = str(date.today())
    return order


def without_product_id():
    order = correct()
    order['products'][0].pop('product_id')
    return order


def without_product_quantity():
    order = correct()
    order['products'][0].pop('quantity')
    return order


def with_too_high_product_quantity():
    order = correct()
    order['products'][0]['quantity'] = 10000
    return order


def populate_with_missing_field():
    return [{k: v for k, v in correct_without_optional().items() if k != key} for key in correct_without_optional()]
