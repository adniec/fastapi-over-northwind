import os

from fastapi import HTTPException
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest
from paypalhttp import HttpError

CLIENT = os.getenv('PAYPAL_CLIENT')
SECRET = os.getenv('PAYPAL_SECRET')

environment = SandboxEnvironment(client_id=CLIENT, client_secret=SECRET)
client = PayPalHttpClient(environment)


async def create_request(amount):
    request = OrdersCreateRequest()
    request.prefer('return=minimal')
    request.request_body({
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {"currency_code": "USD", "value": amount}
        }]
    })
    return request


async def make_request(amount):
    try:
        request = await create_request(amount)
        response = client.execute(request)
        return response.result.id
    except IOError as ioe:
        if isinstance(ioe, HttpError):
            raise HTTPException(status_code=ioe.status_code)


async def is_paid(payment_id):
    try:
        request = OrdersCaptureRequest(payment_id)
        response = client.execute(request)
        if response.result.id == payment_id:
            return True
    except IOError:
        return False
