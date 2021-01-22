#!/bin/bash

# Move file to db container and run.
# To measure time use: sudo time ./report_popularity.sh

for i in $(seq 1 100);
do
  psql -U admin -d northwind -c "SELECT order_details.product_id, products.product_name, categories.category_name, sum(order_details.quantity) AS sold FROM orders JOIN order_details ON orders.order_id = order_details.order_id JOIN products ON products.product_id = order_details.product_id JOIN categories ON products.category_id = categories.category_id WHERE orders.order_date >= '1996-07-10' AND orders.order_date <= '1996-07-17' GROUP BY order_details.product_id, products.product_name, categories.category_name ORDER BY sold DESC"
done
