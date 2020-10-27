import os

from databases import Database
from sqlalchemy import Column, Integer, LargeBinary, MetaData, String, Table, create_engine

from app.api.models import CategoryIn, CategoryOut

DATABASE_URI = os.getenv('DATABASE_URI')

engine = create_engine(DATABASE_URI)
metadata = MetaData()

categories = Table(
    'categories',
    metadata,
    Column('category_id', Integer, primary_key=True),
    Column('category_name', String),
    Column('description', String),
    Column('picture', LargeBinary)
)

database = Database(DATABASE_URI)


async def add_category(payload: CategoryIn):
    query = categories.insert().values(**payload.dict())
    return await database.execute(query=query)
