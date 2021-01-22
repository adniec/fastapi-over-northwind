#!/bin/bash

# Move file to db container and run.
# To measure time use: sudo time ./product_create.sh

for i in $(seq 1 100);
do
  psql -U admin -d northwind -c "INSERT INTO products (product_name, supplier_id, category_id, quantity_per_unit, unit_price, units_in_stock, units_on_order, reorder_level, discontinued) VALUES ('string', 1, 1, 'string', 0, 0, 0, 0, 0)"
done
