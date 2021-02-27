### Measurements

Created to see access time to database through API in comparison to direct queries. Each measured request was called 100 
times. As a direct query in container by using `.sh` script with command `time`. As a `curl` request monitored by 
[Prometheus](https://prometheus.io/) which container is added to   
[docker-compose.yml](https://github.com/ethru/fastapi-over-northwind/blob/master/docker-compose.yml#L153-L166) and 
configuration files are located [here](https://github.com/ethru/fastapi-over-northwind/tree/master/prometheus). After 
building project open `http://0.0.0.0:9000/graph` in browser and write down your query, for example:

![prometheus](img/prometheus.png)

To measure request time we need to import: `from starlette_exporter import PrometheusMiddleware, handle_metrics` in 
service [main file](https://github.com/ethru/fastapi-over-northwind/blob/master/products-service/app/main.py#L2-L12). 
Then we are able to decorate endpoints with `Summary` 
[instance](https://github.com/ethru/fastapi-over-northwind/blob/master/products-service/app/api/products.py#L13) from 
`prometheus_client` module as shown below:

```python
request_metrics = Summary('request_processing_seconds', 'Time spent processing request')


@request_metrics.time()
@products.get('/{product_id}', response_model=ProductOut)
```

To get metrics in `Prometheus UI` query `starlette_request_duration_seconds_sum` was used. Except `delete` where at 
first our results had to be summed by `sum(starlette_request_duration_seconds_sum{method='DELETE'})`.

### Naming

Each measurement is named by endpoint and it links to code. Below database action implementation is shown and printed 
query which is created from it. Test DB refers to `.sh` script used inside database container and Test API to script 
with `curl` requests.



### Results

#### Products CRUD

##### [/api/products/new](https://github.com/ethru/fastapi-over-northwind/blob/master/products-service/app/api/products.py#L43-L47)

[Implementation](https://github.com/ethru/fastapi-over-northwind/blob/master/products-service/app/api/db.py#L31-L38):
```python
async def add_product(payload: ProductIn):
    """Store new product in database."""
    query = products.insert().values(**payload.dict())
    print(query)
    try:
        return await database.execute(query=query)
    except ForeignKeyViolationError:
        raise HTTPException(status_code=422, detail='Wrong foreign key. Record with set id not in database.')
```

Query:

![query](img/tests/query/product_create.png)

[Test DB](https://github.com/ethru/fastapi-over-northwind/blob/master/tests/measurements/db/product_create.sh):

```shell
for i in $(seq 1 100);
do
  psql -U admin -d northwind -c "INSERT INTO products (product_name, supplier_id, category_id, quantity_per_unit, unit_price, units_in_stock, units_on_order, reorder_level, discontinued) VALUES ('string', 1, 1, 'string', 0, 0, 0, 0, 0)"
done
```

![db](img/tests/db/product_create.png)

[Test API](https://github.com/ethru/fastapi-over-northwind/blob/master/tests/measurements/api/product_create.sh):

```shell
for i in $(seq 1 100);
do
  curl -X POST "http://0.0.0.0:8080/api/products/new" -H  "accept: application/json" -H  "Authorization: Bearer Basic YWRtaW46cGFzc3dvcmQ=" -H  "Content-Type: application/json" -d "{\"product_name\":\"string\",\"supplier_id\":1,\"category_id\":1,\"quantity_per_unit\":\"string\",\"unit_price\":0,\"units_in_stock\":0,\"units_on_order\":0,\"reorder_level\":0,\"discontinued\":0}" &
done
```

![api](img/tests/api/product_create.png)

<br />
<br />
<br />
<br />

##### [/api/products/update](https://github.com/ethru/fastapi-over-northwind/blob/master/products-service/app/api/products.py#L51-L55)

[Implementation](https://github.com/ethru/fastapi-over-northwind/blob/master/products-service/app/api/db.py#L41-L50):

```python
async def update(payload: dict):
    """Update product with set id in database."""
    query = products.update().where(products.c.product_id == payload['product_id'])
    payload.pop('product_id')
    query = query.values(**payload).returning(products)
    print(query)
    try:
        return await database.fetch_one(query=query)
    except ForeignKeyViolationError:
        raise HTTPException(status_code=422, detail='Wrong foreign key. Record with set id not in database.')
```

Query:

![query](img/tests/query/product_update.png)

[Test DB](https://github.com/ethru/fastapi-over-northwind/blob/master/tests/measurements/db/product_update.sh):

```shell
for i in $(seq 1 100);
do
  psql -U admin -d northwind -c "UPDATE products SET units_in_stock=100, units_on_order=10 WHERE products.product_id = $i RETURNING products.product_id, products.product_name, products.supplier_id, products.category_id, products.quantity_per_unit, products.unit_price, products.units_in_stock, products.units_on_order, products.reorder_level, products.discontinued"
done
```

![db](img/tests/db/product_update.png)

[Test API](https://github.com/ethru/fastapi-over-northwind/blob/master/tests/measurements/api/product_update.sh):

```shell
for i in $(seq 1 100);
do
  curl -X PUT "http://0.0.0.0:8080/api/products/update" -H  "accept: application/json" -H  "Authorization: Bearer Basic YWRtaW46cGFzc3dvcmQ=" -H  "Content-Type: application/json" -d "{\"product_id\":$i,\"units_in_stock\":100,\"units_on_order\":10}" &
done
```

![api](img/tests/api/product_update.png)

<br />
<br />
<br />
<br />

##### [/api/products/{product_id}](https://github.com/ethru/fastapi-over-northwind/blob/master/products-service/app/api/products.py#L28-L32)

[Implementation](https://github.com/ethru/fastapi-over-northwind/blob/master/products-service/app/api/db.py#L9-L13):
```python
async def get_product(product_id: int):
    """Get product with set id from database."""
    query = products.select().where(products.c.product_id == product_id)
    print(query)
    return await database.fetch_one(query=query)
```

Query:

![query](img/tests/query/product_select.png)

[Test DB](https://github.com/ethru/fastapi-over-northwind/blob/master/tests/measurements/db/product_select.sh):

```shell
for i in $(seq 1 100);
do
  psql -U admin -d northwind -c 'SELECT products.product_id, products.product_name, products.supplier_id, products.category_id, products.quantity_per_unit, products.unit_price, products.units_in_stock, products.units_on_order, products.reorder_level, products.discontinued FROM products WHERE products.product_id = 10'
done
```

![db](img/tests/db/product_select.png)


[Test API](https://github.com/ethru/fastapi-over-northwind/blob/master/tests/measurements/api/product_select.sh):

```shell
for i in $(seq 1 100);
do
  curl -X GET "http://0.0.0.0:8080/api/products/10" -H  "accept: application/json" &
done
```

![api](img/tests/api/product_select.png)

<br />
<br />
<br />
<br />

##### [/api/products/search](https://github.com/ethru/fastapi-over-northwind/blob/master/products-service/app/api/products.py#L36-L39)

[Implementation](https://github.com/ethru/fastapi-over-northwind/blob/master/products-service/app/api/db.py#L16-L28):

```python
async def search(payload: dict):
    """Get products matching payload from database.
    If there is no payload return all products.
    """
    if payload:
        conditions = [getattr(products.c, k) == v for k, v in payload.items()]
        query = select([text('*')]).where(and_(*conditions))
    else:
        query = products.select()

    print(query)
    return await database.fetch_all(query=query)
```

Query:

![query](img/tests/query/product_search.png)

[Test DB](https://github.com/ethru/fastapi-over-northwind/blob/master/tests/measurements/db/product_search.sh):

```shell
for i in $(seq 1 100);
do
  psql -U admin -d northwind -c 'SELECT * FROM products WHERE products.category_id = 7 AND products.discontinued = 0'
done
```

![db](img/tests/db/product_search.png)

[Test API](https://github.com/ethru/fastapi-over-northwind/blob/master/tests/measurements/api/product_search.sh):

```shell
for i in $(seq 1 100);
do
  curl -X POST "http://0.0.0.0:8080/api/products/search" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"category_id\":1,\"units_on_order\":0,\"discontinued\":1}" &
done
```

![api](img/tests/api/product_search.png)

<br />
<br />
<br />
<br />

##### [/api/products/del/{product_id}](https://github.com/ethru/fastapi-over-northwind/blob/master/products-service/app/api/products.py#L59-L63)

[Implementation](https://github.com/ethru/fastapi-over-northwind/blob/master/products-service/app/api/db.py#L53-L60):

```python
async def delete(product_id: int):
    """Remove product with set id from database.
    
    All linked orders and order_details are also deleted (cascade).
    """
    query = products.delete().where(products.c.product_id == product_id).returning(products)
    print(query)
    return await database.fetch_one(query=query)
```

Query:

![query](img/tests/query/product_delete.png)

[Test DB](https://github.com/ethru/fastapi-over-northwind/blob/master/tests/measurements/db/product_delete.sh):

```shell
for i in $(seq 1 100);
do
  psql -U admin -d northwind -c "DELETE FROM products WHERE products.product_id = $i RETURNING products.product_id, products.product_name, products.supplier_id, products.category_id, products.quantity_per_unit, products.unit_price, products.units_in_stock, products.units_on_order, products.reorder_level, products.discontinued"
done
```

![db](img/tests/db/product_delete.png)

[Test API](https://github.com/ethru/fastapi-over-northwind/blob/master/tests/measurements/api/product_delete.sh):

```shell
for i in $(seq 1 100);
do
  curl -X DELETE "http://0.0.0.0:8080/api/products/del/$i" -H  "accept: application/json" -H  "Authorization: Bearer Basic YWRtaW46cGFzc3dvcmQ=" &
done
```

![api](img/tests/api/product_delete.png)

*Prometheus got separate results for `/del/1` ... `/del/100` requests. That's why measurement format differs. Other 
query: `sum(starlette_request_duration_seconds_sum{method='DELETE'})` was used to sum them all.

<br />
<br />
<br />
<br />

#### Reports

##### [/api/reports/customers/profit](https://github.com/ethru/fastapi-over-northwind/blob/master/reports-service/app/api/reports.py#L14-L18)

[Implementation](https://github.com/ethru/fastapi-over-northwind/blob/master/reports-service/app/api/db.py#L63-L87):
```python
async def get_sales_by_customer(from_date, to_date):
    """Return report about sales by customer in set period of time."""
    expression = order_details.c.unit_price * order_details.c.quantity * (1 - order_details.c.discount)
    query = select(
        [
            orders.c.customer_id,
            customers.c.company_name,
            func.round(func.sum(expression)).label('profit')
        ]
    ).select_from(
        join(join(orders, order_details, orders.c.order_id == order_details.c.order_id),
             customers, orders.c.customer_id == customers.c.customer_id)
    ).where(
        and_(
            orders.c.order_date >= from_date,
            orders.c.order_date <= to_date,
        )
    ).group_by(
        orders.c.customer_id,
        customers.c.company_name,
    ).order_by(
        desc('profit')
    )
    print(query)
    return await database.fetch_all(query=query)
```

Query:

![query](img/tests/query/report_profit.png)

[Test DB](https://github.com/ethru/fastapi-over-northwind/blob/master/tests/measurements/db/report_profit.sh):

```shell
for i in $(seq 1 100);
do
  psql -U admin -d northwind -c "SELECT orders.customer_id, customers.company_name, round(sum(order_details.unit_price * order_details.quantity * (1 - order_details.discount))) AS profit FROM orders JOIN order_details ON orders.order_id = order_details.order_id JOIN customers ON orders.customer_id = customers.customer_id WHERE orders.order_date >= '1996-07-10' AND orders.order_date <= '1996-07-17' GROUP BY orders.customer_id, customers.company_name ORDER BY profit DESC"
done
```

![db](img/tests/db/report_profit.png)

[Test API](https://github.com/ethru/fastapi-over-northwind/blob/master/tests/measurements/api/report_profit.sh):

```shell
for i in $(seq 1 100);
do
  curl -X POST "http://0.0.0.0:8080/api/reports/customers/profit" -H  "accept: application/json" -H  "Authorization: Bearer Basic YWRtaW46cGFzc3dvcmQ=" -H  "Content-Type: application/json" -d "{\"from_date\":\"1996-07-10\",\"to_date\":\"1996-07-17\"}" &
done
```

![api](img/tests/api/report_profit.png)

<br />
<br />
<br />
<br />

##### [/api/reports/employees/activity](https://github.com/ethru/fastapi-over-northwind/blob/master/reports-service/app/api/reports.py#L21-L25)

[Implementation](https://github.com/ethru/fastapi-over-northwind/blob/master/reports-service/app/api/db.py#L14-L60):

```python
async def get_employees_activity(from_date, to_date):
    """Return report about employees activity in set period of time."""
    conditions = [
        orders.c.shipped_date >= from_date,
        orders.c.shipped_date <= to_date,
    ]
    return await get_employees_report(conditions)


async def get_employees_report(conditions: list):
    """Return report about employees according to set conditions."""
    query = select(
        [
            orders.c.employee_id,
            await get_full_employee_name(),
            employees.c.title,
            func.count(orders.c.employee_id).label('orders')
        ]
    ).select_from(
        orders.join(
            employees, orders.c.employee_id == employees.c.employee_id
        )
    ).where(
        and_(
            *conditions
        )
    ).group_by(
        orders.c.employee_id,
        employees.c.first_name,
        employees.c.last_name,
        employees.c.title,
        employees.c.title_of_courtesy
    ).order_by(
        desc('orders')
    )
    print(query)
    return await database.fetch_all(query=query)


#Helper function to format employee data
async def get_full_employee_name():
    """Return concat function with full employee name."""
    blank = text("' '")
    full_name = [employees.c.title_of_courtesy, blank, employees.c.first_name, blank, employees.c.last_name]
    return func.concat(*full_name).label('employee')
```

Query:

![query](img/tests/query/report_activity.png)

[Test DB](https://github.com/ethru/fastapi-over-northwind/blob/master/tests/measurements/db/report_activity.sh):

```shell
for i in $(seq 1 100);
do
  psql -U admin -d northwind -c "SELECT orders.employee_id, concat(employees.title_of_courtesy, ' ', employees.first_name, ' ', employees.last_name) AS employee, employees.title, count(orders.employee_id) AS orders FROM orders JOIN employees ON orders.employee_id = employees.employee_id WHERE orders.shipped_date >= '1996-07-10' AND orders.shipped_date <= '1996-07-17' GROUP BY orders.employee_id, employees.first_name, employees.last_name, employees.title, employees.title_of_courtesy ORDER BY orders DESC"
done
```

![db](img/tests/db/report_activity.png)

[Test API](https://github.com/ethru/fastapi-over-northwind/blob/master/tests/measurements/api/report_activity.sh):

```shell
for i in $(seq 1 100);
do
  curl -X POST "http://0.0.0.0:8080/api/reports/employees/activity" -H  "accept: application/json" -H  "Authorization: Bearer Basic YWRtaW46cGFzc3dvcmQ=" -H  "Content-Type: application/json" -d "{\"from_date\":\"1996-07-10\",\"to_date\":\"1996-07-17\"}" &
done
```

![api](img/tests/api/report_activity.png)

<br />
<br />
<br />
<br />

##### [/api/reports/employees/delays](https://github.com/ethru/fastapi-over-northwind/blob/master/reports-service/app/api/reports.py#L28-L32)

[Implementation](https://github.com/ethru/fastapi-over-northwind/blob/master/reports-service/app/api/db.py#L23-L60):
```python
async def get_employees_shipment_delays(from_date, to_date):
    """Return report about employees shipment delays in set period of time."""
    conditions = [
        orders.c.shipped_date >= from_date,
        orders.c.shipped_date <= to_date,
        orders.c.shipped_date > orders.c.required_date
    ]
    return await get_employees_report(conditions)


async def get_employees_report(conditions: list):
    """Return report about employees according to set conditions."""
    query = select(
        [
            orders.c.employee_id,
            await get_full_employee_name(),
            employees.c.title,
            func.count(orders.c.employee_id).label('orders')
        ]
    ).select_from(
        orders.join(
            employees, orders.c.employee_id == employees.c.employee_id
        )
    ).where(
        and_(
            *conditions
        )
    ).group_by(
        orders.c.employee_id,
        employees.c.first_name,
        employees.c.last_name,
        employees.c.title,
        employees.c.title_of_courtesy
    ).order_by(
        desc('orders')
    )
    print(query)
    return await database.fetch_all(query=query)


#Helper function to format employee data
async def get_full_employee_name():
    """Return concat function with full employee name."""
    blank = text("' '")
    full_name = [employees.c.title_of_courtesy, blank, employees.c.first_name, blank, employees.c.last_name]
    return func.concat(*full_name).label('employee')
```

Query:

![query](img/tests/query/report_delays.png)

[Test DB](https://github.com/ethru/fastapi-over-northwind/blob/master/tests/measurements/db/report_delays.sh):

```shell
for i in $(seq 1 100);
do
  psql -U admin -d northwind -c "SELECT orders.employee_id, concat(employees.title_of_courtesy, ' ', employees.first_name, ' ', employees.last_name) AS employee, employees.title, count(orders.employee_id) AS orders FROM orders JOIN employees ON orders.employee_id = employees.employee_id WHERE orders.shipped_date >= '1996-07-10' AND orders.shipped_date <= '1997-07-17' AND orders.shipped_date > orders.required_date GROUP BY orders.employee_id, employees.first_name, employees.last_name, employees.title, employees.title_of_courtesy ORDER BY orders DESC"
done
```

![db](img/tests/db/report_delays.png)


[Test API](https://github.com/ethru/fastapi-over-northwind/blob/master/tests/measurements/api/report_delays.sh):

```shell
for i in $(seq 1 100);
do
  curl -X POST "http://0.0.0.0:8080/api/reports/employees/delays" -H  "accept: application/json" -H  "Authorization: Bearer Basic YWRtaW46cGFzc3dvcmQ=" -H  "Content-Type: application/json" -d "{\"from_date\":\"1996-07-10\",\"to_date\":\"1997-07-17\"}" &
done
```

![api](img/tests/api/report_delays.png)

<br />
<br />
<br />
<br />

##### [/api/reports/products/popularity](https://github.com/ethru/fastapi-over-northwind/blob/master/reports-service/app/api/reports.py#L35-L39)

[Implementation](https://github.com/ethru/fastapi-over-northwind/blob/master/reports-service/app/api/db.py#L90-L116):

```python
async def get_products_by_popularity(from_date, to_date):
    """Return report about products by popularity in set period of time."""
    query = select(
        [
            order_details.c.product_id,
            products.c.product_name,
            categories.c.category_name,
            func.sum(order_details.c.quantity).label('sold')
        ]
    ).select_from(
        join(join(join(orders, order_details, orders.c.order_id == order_details.c.order_id),
                  products, products.c.product_id == order_details.c.product_id),
             categories, products.c.category_id == categories.c.category_id)
    ).where(
        and_(
            orders.c.order_date >= from_date,
            orders.c.order_date <= to_date,
        )
    ).group_by(
        order_details.c.product_id,
        products.c.product_name,
        categories.c.category_name,
    ).order_by(
        desc('sold')
    )
    print(query)
    return await database.fetch_all(query=query)
```

Query:

![query](img/tests/query/report_popularity.png)

[Test DB](https://github.com/ethru/fastapi-over-northwind/blob/master/tests/measurements/db/report_popularity.sh):

```shell
for i in $(seq 1 100);
do
  psql -U admin -d northwind -c "SELECT order_details.product_id, products.product_name, categories.category_name, sum(order_details.quantity) AS sold FROM orders JOIN order_details ON orders.order_id = order_details.order_id JOIN products ON products.product_id = order_details.product_id JOIN categories ON products.category_id = categories.category_id WHERE orders.order_date >= '1996-07-10' AND orders.order_date <= '1996-07-17' GROUP BY order_details.product_id, products.product_name, categories.category_name ORDER BY sold DESC"
done
```

![db](img/tests/db/report_popularity.png)

[Test API](https://github.com/ethru/fastapi-over-northwind/blob/master/tests/measurements/api/report_popularity.sh):

```shell
for i in $(seq 1 100);
do
  curl -X POST "http://0.0.0.0:8080/api/reports/products/popularity" -H  "accept: application/json" -H  "Authorization: Bearer Basic YWRtaW46cGFzc3dvcmQ=" -H  "Content-Type: application/json" -d "{\"from_date\":\"1996-07-10\",\"to_date\":\"1996-07-17\"}" &
done
```

![api](img/tests/api/report_popularity.png)

<br />
<br />
<br />
<br />

##### [/api/reports/products/reorder](https://github.com/ethru/fastapi-over-northwind/blob/master/reports-service/app/api/reports.py#L42-L46)

[Implementation](https://github.com/ethru/fastapi-over-northwind/blob/master/reports-service/app/api/db.py#L119-L148):

```python
async def get_products_to_reorder():
    """Return report about products to reorder."""
    available = products.c.units_in_stock - products.c.units_on_order
    contact = func.concat(suppliers.c.contact_title, text("': '"), suppliers.c.contact_name,
                          text("' via '"), suppliers.c.phone)
    to_reorder = available - products.c.reorder_level

    query = select(
        [
            products.c.product_id,
            products.c.product_name,
            categories.c.category_name,
            products.c.units_in_stock,
            products.c.units_on_order,
            available.label('units_available'),
            products.c.reorder_level,
            suppliers.c.company_name.label('supplier'),
            contact.label('contact')
        ]
    ).select_from(
        join(join(products, suppliers, products.c.supplier_id == suppliers.c.supplier_id),
             categories, products.c.category_id == categories.c.category_id)
    ).where(
        and_(
            products.c.discontinued == 0,
            to_reorder <= 0
        )
    )
    print(query)
    return await database.fetch_all(query=query)
```

Query:

![query](img/tests/query/report_reorder.png)

[Test DB](https://github.com/ethru/fastapi-over-northwind/blob/master/tests/measurements/db/report_reorder.sh):

```shell
for i in $(seq 1 100);
do
  psql -U admin -d northwind -c "SELECT products.product_id, products.product_name, categories.category_name, products.units_in_stock, products.units_on_order, products.units_in_stock - products.units_on_order AS units_available, products.reorder_level, suppliers.company_name AS supplier, concat(suppliers.contact_title, ': ', suppliers.contact_name, ' via ', suppliers.phone) AS contact FROM products JOIN suppliers ON products.supplier_id = suppliers.supplier_id JOIN categories ON products.category_id = categories.category_id WHERE products.discontinued = 0 AND (products.units_in_stock - products.units_on_order) - products.reorder_level <= 0"
done
```

![db](img/tests/db/report_reorder.png)

[Test API](https://github.com/ethru/fastapi-over-northwind/blob/master/tests/measurements/api/report_reorder.sh):

```shell
for i in $(seq 1 100);
do
  curl -X GET "http://0.0.0.0:8080/api/reports/products/reorder" -H  "accept: application/json" -H  "Authorization: Bearer Basic YWRtaW46cGFzc3dvcmQ=" &
done
```

![api](img/tests/api/report_reorder.png)
