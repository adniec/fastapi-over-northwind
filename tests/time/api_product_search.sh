#!/bin/bash

for i in $(seq 1 100);
do
  curl -X POST "http://0.0.0.0:8080/api/products/search" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"category_id\":1,\"units_on_order\":0,\"discontinued\":1}" &
done
