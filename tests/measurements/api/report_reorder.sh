#!/bin/bash

for i in $(seq 1 100);
do
  curl -X GET "http://0.0.0.0:8080/api/reports/products/reorder" -H  "accept: application/json" -H  "Authorization: Bearer Basic YWRtaW46cGFzc3dvcmQ=" &
done
