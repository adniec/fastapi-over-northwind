import os

from databases import Database
from sqlalchemy import Column, Integer, LargeBinary, MetaData, String, Table, create_engine

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
