#!/bin/bash

# Move file to db container and run.
# To measure time use: sudo time ./db_product_delete.sh

for i in $(seq 1 100);
do
  psql -U northwind_user -d northwind -c "DELETE FROM products WHERE product_id = $i RETURNING *"
done
