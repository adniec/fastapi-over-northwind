from fastapi import HTTPException

from app.api import database
from app.api.models import products, ProductUpdate


async def select_for_update(product_id: int):
    """Select product by id for update."""
    query = products.select(for_update=True).where(products.c.product_id == product_id)
    return await database.fetch_one(query=query)


async def update(data: ProductUpdate) -> int:
    """Update product with set id in database."""
    query = products.update().where(
        products.c.product_id == data.product_id
    ).values(**data.dict(exclude_unset=True)).returning(products)
    return await database.execute(query=query)


async def check_availability(product, quantity):
    """Raise exception when there is not enough product units."""
    available = product['units_in_stock'] - product['units_on_order']
    if available < quantity:
        raise HTTPException(status_code=422, detail=f'Not enough available {product["product_name"]} units.')


async def order(product_id: int, quantity: int):
    """Order product in set quantity.

    Return unit price if units are available in stock. Update units_on_order in product details.
    """
    product = await select_for_update(product_id)
    if not product:
        raise HTTPException(status_code=404, detail='Product with set id not found.')
    await check_availability(product, quantity)

    data = ProductUpdate(product_id=product_id, units_on_order=product['units_on_order'] + quantity)
    await update(data)
    return product['unit_price']


async def send(product_id: int, quantity: int):
    """Reduce units on order and units in stock by set quantity."""
    product = await select_for_update(product_id)

    data = ProductUpdate(
        product_id=product_id,
        units_in_stock=product['units_in_stock'] - quantity,
        units_on_order=product['units_on_order'] - quantity
    )
    await update(data)


async def cancel(product_id: int, quantity: int):
    """Reduce units on order by set quantity."""
    product = await select_for_update(product_id)

    data = ProductUpdate(product_id=product_id, units_on_order=product['units_on_order'] - quantity)
    await update(data)
