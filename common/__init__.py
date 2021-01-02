import os

from databases import Database
from sqlalchemy import MetaData, create_engine

DATABASE_URI = os.getenv('DATABASE_URI')

engine = create_engine(DATABASE_URI)
metadata = MetaData()

database = Database(DATABASE_URI)
