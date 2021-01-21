#!/bin/bash

# Move file to db container and run.
# To measure time use: sudo time ./product_delete.sh

for i in $(seq 1 100);
do
  psql -U northwind_user -d northwind -c "DELETE FROM products WHERE products.product_id = $i RETURNING products.product_id, products.product_name, products.supplier_id, products.category_id, products.quantity_per_unit, products.unit_price, products.units_in_stock, products.units_on_order, products.reorder_level, products.discontinued"
done
