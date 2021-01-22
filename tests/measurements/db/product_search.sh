#!/bin/bash

# Move file to db container and run.
# To measure time use: sudo time ./product_search.sh

for i in $(seq 1 100);
do
  psql -U admin -d northwind -c 'SELECT * FROM products WHERE products.category_id = 7 AND products.discontinued = 0'
done
