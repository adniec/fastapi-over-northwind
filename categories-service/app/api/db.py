import os

from databases import Database
from sqlalchemy import Column, Integer, LargeBinary, MetaData, String, Table, create_engine

from app.api.models import CategoryIn

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


async def get_category(category_id: int):
    """Get category with set id from database."""
    return await database.fetch_one(query=categories.select().where(categories.c.category_id == category_id))


async def get_categories():
    """Get all categories stored in database."""
    return await database.fetch_all(query=categories.select())


async def add_category(payload: CategoryIn):
    """Store new category in database."""
    query = categories.insert().values(**payload.dict())
    return await database.execute(query=query)


async def get_unlisted_category():
    """Return id of UNLISTED category.

    If category does not exist then create it.
    """
    name = 'UNLISTED'
    query = 'SELECT category_id FROM categories WHERE category_name=:name'
    unlisted = await database.fetch_one(query=query, values={'name': name})
    if unlisted:
        return unlisted['category_id']

    unlisted = CategoryIn(category_name=name, description='', picture='')
    return await add_category(unlisted)


async def update(category_id: int, payload: CategoryIn):
    """Update category with set id in database."""
    query = categories.update().where(
        categories.c.category_id == category_id
    ).values(**payload.dict()).returning(categories)
    return await database.execute(query=query)


@database.transaction()
async def delete(category_id: int):
    """Remove category with set id from database.

    Unlink all products connected to that category by replacing category_id with id of unlisted category.
    """
    empty = await get_unlisted_category()
    query = "UPDATE products SET category_id = :empty WHERE category_id = :id"
    await database.execute(query=query, values={'empty': empty, 'id': category_id})

    query = categories.delete().where(categories.c.category_id == category_id).returning(categories)
    return await database.execute(query=query)
