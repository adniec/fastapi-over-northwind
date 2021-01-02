from app.api import database

from app.api.models import products


async def search(payload: dict):
    if not payload:
        return await database.fetch_all(query=products.select())

    payload = {k: f"'{v}'" if isinstance(v, str) else v for k, v in payload.items()}
    condition = ' AND '.join([f'{k}={v}' for k, v in payload.items()])
    query = f'SELECT * FROM products WHERE {condition}'
    result = []
    async for row in database.iterate(query=query):
        result.append(row)
    return result
