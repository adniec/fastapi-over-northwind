#!/bin/bash

# Move file to db container and run.
# To measure time use: sudo time ./db_product_update.sh

for i in $(seq 1 100);
do
  psql -U northwind_user -d northwind -c "UPDATE products SET units_in_stock = 100, units_on_order = 10 WHERE product_id = $i RETURNING *"
done
