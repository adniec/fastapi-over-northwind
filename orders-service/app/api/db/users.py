import random

from app.api import database
from app.api.models import customers, employees, shippers


async def get_customer_by_id(customer_id: str):
    """Get customer details from database by set id."""
    return await database.fetch_one(query=customers.select().where(customers.c.customer_id == customer_id))


async def get_employee():
    """Return id of randomly picked sales representative."""
    sales = await database.fetch_all(query=employees.select().where(employees.c.title == 'Sales Representative'))
    return random.choice(sales)['employee_id']


async def get_shippers():
    """Return shippers data."""
    return await database.fetch_all(query=shippers.select())
