#!/bin/bash

# Move file to db container and run.
# To measure time use: sudo time ./db_product_create.sh

for i in $(seq 1 100);
do
  psql -U northwind_user -d northwind -c "INSERT INTO products VALUES (DEFAULT, 'string', 1, 1, 'string', 0, 0, 0, 0, 0)"
done
