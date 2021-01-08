#!/bin/bash

for i in $(seq 1 100);
do
  curl -X POST "http://0.0.0.0:8080/api/products/new" -H  "accept: application/json" -H  "Authorization: Bearer Basic YWRtaW46cGFzc3dvcmQ=" -H  "Content-Type: application/json" -d "{\"product_name\":\"string\",\"supplier_id\":1,\"category_id\":1,\"quantity_per_unit\":\"string\",\"unit_price\":0,\"units_in_stock\":0,\"units_on_order\":0,\"reorder_level\":0,\"discontinued\":0}" &
done
