def from_db():
    return {
        'product_name': 'Chai',
        'supplier_id': 8,
        'category_id': 1,
        'quantity_per_unit': '10 boxes x 30 bags',
        'unit_price': 18,
        'units_in_stock': 39,
        'units_on_order': 0,
        'reorder_level': 10,
        'discontinued': 1,
        'product_id': 1
    }


def with_wrong_types():
    product = from_db()
    product.pop('product_name')
    product.pop('quantity_per_unit')
    return {k: 'Test' for k in product.keys()}


def new():
    product = from_db()
    product.pop('product_id')
    product['product_name'] = 'Test'
    return product


def populate_with_missing_field():
    return [{k: v for k, v in new().items() if k != key} for key in new()]


def populate_with_wrong_field():
    wrong = with_wrong_types()
    wrong.pop('product_id')
    return [{k: v if k != key else wrong[key] for k, v in new().items()} for key in wrong]
