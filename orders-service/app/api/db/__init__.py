from app.api import database
from app.api.db import orders
from app.api.db import products
from app.api.db import users


@database.transaction()
async def process_order(order_id: int, remove: bool):
    """Cancel order if remove flag set to True otherwise send order and update products."""
    details = await orders.get_details_by_id(order_id)

    for data in details:
        await (products.cancel if remove else products.send)(data['product_id'], data['quantity'])

    result = await orders.update({'order_id': order_id, 'status': 'CANCELED' if remove else 'SENT'})
    if result == order_id:
        return True
    return False
