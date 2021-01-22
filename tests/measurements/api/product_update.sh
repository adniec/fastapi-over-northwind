#!/bin/bash

for i in $(seq 1 100);
do
  curl -X PUT "http://0.0.0.0:8080/api/products/update" -H  "accept: application/json" -H  "Authorization: Bearer Basic YWRtaW46cGFzc3dvcmQ=" -H  "Content-Type: application/json" -d "{\"product_id\":$i,\"units_in_stock\":100,\"units_on_order\":10}" &
done
