#!/bin/bash

# Move file to db container and run.
# To measure time use: sudo time ./report_activity.sh

for i in $(seq 1 100);
do
  psql -U admin -d northwind -c "SELECT orders.employee_id, concat(employees.title_of_courtesy, ' ', employees.first_name, ' ', employees.last_name) AS employee, employees.title, count(orders.employee_id) AS orders FROM orders JOIN employees ON orders.employee_id = employees.employee_id WHERE orders.shipped_date >= '1996-07-10' AND orders.shipped_date <= '1996-07-17' GROUP BY orders.employee_id, employees.first_name, employees.last_name, employees.title, employees.title_of_courtesy ORDER BY orders DESC"
done
