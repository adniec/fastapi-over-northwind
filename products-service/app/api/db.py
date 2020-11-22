import os

from databases import Database
from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine

DATABASE_URI = os.getenv('DATABASE_URI')

engine = create_engine(DATABASE_URI)
metadata = MetaData()

products = Table(
    'products',
    metadata,
    Column('product_id', Integer, primary_key=True),
    Column('product_name', String),
    Column('supplier_id', Integer),
    Column('category_id', Integer),
    Column('quantity_per_unit', String),
    Column('unit_price', Integer),
    Column('units_in_stock', Integer),
    Column('units_on_order', Integer),
    Column('reorder_level', Integer),
    Column('discontinued', Integer),
)

database = Database(DATABASE_URI)


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
