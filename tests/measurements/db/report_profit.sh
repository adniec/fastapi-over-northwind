#!/bin/bash

# Move file to db container and run.
# To measure time use: sudo time ./report_profit.sh

for i in $(seq 1 100);
do
  psql -U admin -d northwind -c "SELECT orders.customer_id, customers.company_name, round(sum(order_details.unit_price * order_details.quantity * (1 - order_details.discount))) AS profit FROM orders JOIN order_details ON orders.order_id = order_details.order_id JOIN customers ON orders.customer_id = customers.customer_id WHERE orders.order_date >= '1996-07-10' AND orders.order_date <= '1996-07-17' GROUP BY orders.customer_id, customers.company_name ORDER BY profit DESC"
done
