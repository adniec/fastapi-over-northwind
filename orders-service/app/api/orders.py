from datetime import date
from typing import List

import asyncio
from fastapi import APIRouter, Depends, HTTPException
from prometheus_client import Summary

from app.api import db
from app.api.auth import authorize
from app.api.models import Address, Order, OrderDetails, OrderIn, OrderOut, OrderSend
from app.api.payments import is_paid

orders = APIRouter()
loop = asyncio.get_event_loop()

PAY_URL = 'https://www.sandbox.paypal.com/checkoutnow?token='

request_metrics = Summary('request_processing_seconds', 'Time spent processing request')


async def get_customer_address(customer_id: str) -> Address:
    """Return formatted customer address."""
    customer = await db.users.get_customer_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail='Customer with set id not found.')
    return Address(**customer)


async def check_shipper(shipper_id: int):
    """Raise exception when shipper id is not in database."""
    shippers = await db.users.get_shippers()
    if not (shipper_id in [x['shipper_id'] for x in shippers]):
        raise HTTPException(status_code=404, detail='Shipper id not found. Please provide correct one.')


async def check_order_to_send(order_id: int):
    """Raise exception if order with set id does not exists or if it has wrong status."""
    order = await db.orders.get_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail='Order with set id not found.')
    if not order['status'] == 'PAID':
        raise HTTPException(status_code=422, detail='Order cannot be send. Status not PAID.')


async def prepare_order(payload: Order) -> OrderIn:
    """Fill all additional data needed to make an order."""
    address = await get_customer_address(payload.customer_id)
    if payload.address:
        address = payload.address

    await check_shipper(payload.ship_via)
    employee = await db.users.get_employee()
    return OrderIn(employee_id=employee, order_date=date.today(), **payload.dict(), **address.dict())


async def process_payment_status(order_id, payment_id, calls=3):
    """Check payment status.

    If it is correct make update in database otherwise calls self again. After few calls cancel order and update data.
    """
    await asyncio.sleep(10)
    if await is_paid(payment_id):
        await db.orders.update({'order_id': order_id, 'status': 'PAID'})
        return True
    if calls:
        loop.create_task(process_payment_status(order_id, payment_id, calls - 1))
    else:
        return await db.process_order(order_id, True)


@orders.get('/shippers')
async def list_shippers():
    """Return list with available shippers."""
    return await db.users.get_shippers()


@orders.get('/all', response_model=List[OrderOut], dependencies=[Depends(authorize)])
async def get_all():
    """Return all orders stored in database."""
    return await db.orders.get_all()


@orders.get('/details/{order_id}', response_model=List[OrderDetails], dependencies=[Depends(authorize)])
async def get_details(order_id: int):
    """Return order details from passed id."""
    details = await db.orders.get_details_by_id(order_id)
    if not details:
        raise HTTPException(status_code=404, detail='Order not found.')
    return details


@orders.post('/make', dependencies=[Depends(authorize)])
async def make_order(payload: Order):
    """Make order for products."""
    details = await prepare_order(payload)
    payment = await db.orders.make(payload.products, details)
    loop.create_task(process_payment_status(**payment))
    return PAY_URL + payment['payment_id']


@orders.get('/send/{order_id}/{freight}', dependencies=[Depends(authorize)])
async def send(order_id: int, freight: float):
    """Change order status to SENT and set freight."""
    await check_order_to_send(order_id)
    order = OrderSend(order_id=order_id, shipped_date=date.today(), freight=freight)

    if not await db.orders.update(order.dict()):
        raise HTTPException(status_code=503, detail='Something went wrong. Try again later.')
    return await db.process_order(order_id, False)
