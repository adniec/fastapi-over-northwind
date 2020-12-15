import os

from sqlalchemy import MetaData, create_engine
from databases import Database

DATABASE_URI = os.getenv('DATABASE_URI')

engine = create_engine(DATABASE_URI)
metadata = MetaData()

database = Database(DATABASE_URI)
