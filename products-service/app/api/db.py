from asyncpg.exceptions import ForeignKeyViolationError
from fastapi import HTTPException

from app.api import database
from app.api.models import ProductIn, ProductOut, products


async def get_product(product_id: int):
    """Get product with set id from database."""
    return await database.fetch_one(query=products.select().where(products.c.product_id == product_id))


async def search(payload: dict):
    """Get products matching payload from database.

    If there is no payload return all products.
    """
    if not payload:
        return await database.fetch_all(query=products.select())

    payload = {k: f"'{v}'" if isinstance(v, str) else v for k, v in payload.items()}
    condition = ' AND '.join([f'{k}={v}' for k, v in payload.items()])
    query = f'SELECT * FROM products WHERE {condition}'
    result = []
    async for row in database.iterate(query=query):
        result.append(row)
    return result


async def add_product(payload: ProductIn):
    """Store new product in database."""
    query = products.insert().values(**payload.dict())
    try:
        return await database.execute(query=query)
    except ForeignKeyViolationError:
        raise HTTPException(status_code=422, detail='Wrong foreign key. Record with set id not in database.')


async def update(payload: ProductOut):
    """Update product with set id in database."""
    query = products.update().where(
        products.c.product_id == payload.product_id
    ).values(**payload.dict()).returning(products)
    try:
        return await database.execute(query=query)
    except ForeignKeyViolationError:
        raise HTTPException(status_code=422, detail='Wrong foreign key. Record with set id not in database.')


async def delete(product_id: int):
    """Remove product with set id from database.

    All linked orders and order_details are also deleted (cascade).
    """
    query = products.delete().where(products.c.product_id == product_id).returning(products)
    return await database.execute(query=query)
