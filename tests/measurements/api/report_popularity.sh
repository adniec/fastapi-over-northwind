#!/bin/bash

for i in $(seq 1 100);
do
  curl -X POST "http://0.0.0.0:8080/api/reports/products/popularity" -H  "accept: application/json" -H  "Authorization: Bearer Basic YWRtaW46cGFzc3dvcmQ=" -H  "Content-Type: application/json" -d "{\"from_date\":\"1996-07-10\",\"to_date\":\"1996-07-17\"}" &
done
