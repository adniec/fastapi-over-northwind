#!/bin/bash

# Move file to db container and run.
# To measure time use: sudo time ./report_reorder.sh

for i in $(seq 1 100);
do
  psql -U admin -d northwind -c "SELECT products.product_id, products.product_name, categories.category_name, products.units_in_stock, products.units_on_order, products.units_in_stock - products.units_on_order AS units_available, products.reorder_level, suppliers.company_name AS supplier, concat(suppliers.contact_title, ': ', suppliers.contact_name, ' via ', suppliers.phone) AS contact FROM products JOIN suppliers ON products.supplier_id = suppliers.supplier_id JOIN categories ON products.category_id = categories.category_id WHERE products.discontinued = 0 AND (products.units_in_stock - products.units_on_order) - products.reorder_level <= 0"
done
