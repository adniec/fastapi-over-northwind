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
    products = []
    for key in new():
        product = new()
        product.pop(key)
        products.append(product)
    return products


def populate_with_wrong_field():
    base = with_wrong_types()
    base.pop('product_id')
    products = []
    for key in base:
        product = new()
        product[key] = base[key]
        products.append(product)
    return products
