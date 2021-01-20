def correct():
    return {
        'from_date': '1996-07-10',
        'to_date': '1996-07-17'
    }


def correct_in_seconds():
    return {
        'from_date': 1,
        'to_date': 1485714600
    }


def with_wrong_values():
    return {
        'from_date': 'abc',
        'to_date': 'abc'
    }


def with_higher_from_date():
    return {
        'from_date': '1996-07-17',
        'to_date': '1996-07-10'
    }


def populate_with_missing_field():
    return [{k: v for k, v in correct().items() if k != key} for key in correct()]
