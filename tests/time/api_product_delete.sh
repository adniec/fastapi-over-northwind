#!/bin/bash

for i in $(seq 1 100);
do
  curl -X DELETE "http://0.0.0.0:8080/api/products/del/$i" -H  "accept: application/json" -H  "Authorization: Bearer Basic YWRtaW46cGFzc3dvcmQ=" &
done
