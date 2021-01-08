#!/bin/bash

# Move file to db container and run.
# To measure time use: sudo time ./db_product_select.sh

for i in $(seq 1 100);
do
  psql -U northwind_user -d northwind -c 'SELECT * FROM products WHERE product_id = 10'
done
