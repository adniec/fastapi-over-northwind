from datetime import date
from typing import List, Optional

from pydantic import BaseModel, validator
from sqlalchemy import Column, Date, Float, ForeignKeyConstraint, Integer, String, Table

from app.api import metadata

customers = Table(
    'customers',
    metadata,
    Column('customer_id', String, primary_key=True),
    Column('company_name', String),
    Column('address', String),
    Column('city', String),
    Column('region', String),
    Column('postal_code', String),
    Column('country', String),
)

employees = Table(
    'employees',
    metadata,
    Column('employee_id', Integer, primary_key=True),
    Column('title', String),
)

orders = Table(
    'orders',
    metadata,
    Column('order_id', Integer, primary_key=True),
    Column('customer_id', String, primary_key=True),
    Column('employee_id', Integer, primary_key=True),
    Column('order_date', Date),
    Column('required_date', Date, nullable=True),
    Column('shipped_date', Date, nullable=True),
    Column('ship_via', Integer, primary_key=True),
    Column('freight', Float, nullable=True),
    Column('ship_name', String),
    Column('ship_address', String),
    Column('ship_city', String),
    Column('ship_region', String),
    Column('ship_postal_code', String),
    Column('ship_country', String),
    Column('paypal_id', String, nullable=True),
    Column('status', String, nullable=True),
    ForeignKeyConstraint(['customer_id'], ['customers.customer_id']),
    ForeignKeyConstraint(['employee_id'], ['employees.employee_id']),
    ForeignKeyConstraint(['ship_via'], ['shippers.shipper_id'])
)

order_details = Table(
    'order_details',
    metadata,
    Column('order_id', Integer, primary_key=True),
    Column('product_id', Integer, primary_key=True),
    Column('unit_price', Integer),
    Column('quantity', Integer),
    Column('discount', Integer),
    ForeignKeyConstraint(['order_id'], ['orders.order_id']),
    ForeignKeyConstraint(['product_id'], ['products.product_id'])
)

shippers = Table(
    'shippers',
    metadata,
    Column('shipper_id', Integer, primary_key=True),
    Column('company_name', String),
    Column('phone', String),
)

products = Table(
    'products',
    metadata,
    Column('product_id', Integer, primary_key=True),
    Column('product_name', String),
    Column('unit_price', Integer),
    Column('units_in_stock', Integer),
    Column('units_on_order', Integer)
)


class Address(BaseModel):
    ship_name: str
    ship_address: str
    ship_city: str
    ship_region: Optional[str]
    ship_postal_code: Optional[str]
    ship_country: str

    class Config:
        allow_population_by_field_name = True
        fields = {
            'ship_name': 'company_name',
            'ship_address': 'address',
            'ship_city': 'city',
            'ship_region': 'region',
            'ship_postal_code': 'postal_code',
            'ship_country': 'country'
        }


class Product(BaseModel):
    product_id: int
    quantity: int


class ProductUpdate(BaseModel):
    product_id: int
    units_in_stock: Optional[int]
    units_on_order: Optional[int]


class OrderDetails(Product):
    order_id: int
    unit_price: float
    discount: Optional[float] = 0


class Order(BaseModel):
    customer_id: str
    required_date: Optional[date] = None
    ship_via: int
    address: Optional[Address] = None
    products: List[Product]

    @validator('required_date')
    def value_must_be_greater_than_0(cls, required):
        if date.today() < required:
            return required
        raise ValueError('required date must be greater than order date')


class OrderIn(BaseModel):
    customer_id: str
    employee_id: int
    order_date: date
    required_date: Optional[date]
    shipped_date: Optional[date]
    ship_via: int
    freight: Optional[float]
    ship_name: str
    ship_address: str
    ship_city: str
    ship_region: Optional[str]
    ship_postal_code: Optional[str]
    ship_country: str
    paypal_id: Optional[str]
    status: Optional[str]


class OrderOut(OrderIn):
    order_id: int


class OrderSend(BaseModel):
    order_id: int
    shipped_date: date
    freight: float
    status: str
