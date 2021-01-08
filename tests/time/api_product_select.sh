#!/bin/bash

for i in $(seq 1 100);
do
  curl -X GET "http://0.0.0.0:8080/api/products/10" -H  "accept: application/json" &
done
