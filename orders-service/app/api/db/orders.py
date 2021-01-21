from asyncpg.exceptions import ForeignKeyViolationError
from typing import List

from fastapi import HTTPException

from app.api import database
from app.api.db.products import order
from app.api.models import orders, order_details, OrderIn, OrderDetails, Product
from app.api.payments import make_request


async def get_all():
    """Get all orders stored in database."""
    return await database.fetch_all(query=orders.select())


async def get_by_id(order_id):
    """Get order stored in database by id."""
    return await database.fetch_one(query=orders.select().where(orders.c.order_id == order_id))


async def get_details_by_id(order_id):
    """Get order details stored in database from set id."""
    return await database.fetch_all(query=order_details.select().where(order_details.c.order_id == order_id))


async def add_order(payload: OrderIn):
    """Create new empty order in database and return its id."""
    query = orders.insert().values(**payload.dict()).returning(orders)
    return await database.execute(query=query)


async def add_order_details(details: OrderDetails):
    """Create new empty order in database and return its id."""
    query = order_details.insert().values(**details.dict()).returning(order_details)
    return await database.execute(query=query)


async def update(payload: dict):
    """Update order with set id by payload."""
    query = orders.update().where(
        orders.c.order_id == payload['order_id']
    ).values(**payload).returning(orders)
    return await database.execute(query=query)


async def check_query_result(result):
    """Raise exception when there is no result from database."""
    if not result:
        raise HTTPException(status_code=503)


@database.transaction()
async def make(products: List[Product], user_data: OrderIn):
    """Create order in database.

    Fill order details with products. Set units on order. Make payment request via Paypal. Return dict with order_id and
    payment_id.
    """
    try:
        order_id = await add_order(user_data)
    except ForeignKeyViolationError:
        raise HTTPException(status_code=404, detail='Shipper with set id not found.')
    total_cash = 0

    for product in products:
        unit_price = await order(product.product_id, product.quantity)

        details = OrderDetails(order_id=order_id, unit_price=unit_price, **product.dict())
        await check_query_result(await add_order_details(details))

        cash = product.quantity * unit_price
        total_cash += cash

    payment_id = await make_request(total_cash)
    result = await update({'order_id': order_id, 'paypal_id': payment_id, 'status': 'PENDING'})
    await check_query_result(result)
    return {'order_id': order_id, 'payment_id': payment_id}
