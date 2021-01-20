def from_db():
    return {
        'category_name': 'Beverages',
        'description': 'Soft drinks, coffees, teas, beers, and ales',
        'picture': '',
        'category_id': 1
    }


def new():
    category = from_db()
    category.pop('category_id')
    category['category_name'] = 'Test'
    return category


def populate_with_missing_field():
    return [{k: v for k, v in new().items() if k != key} for key in new()]
