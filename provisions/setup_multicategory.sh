#!/bin/bash

echo
echo "=================================="
echo "===== Creating MultiCategory ====="
echo "=================================="

docker pull valteruo/multicategory
docker image tag valteruo/multicategory:latest multicategory
docker run -it --publish 8090:8050 --detach --rm --net=multicategory --name multicategory-running multicategory

echo
echo "================================================="
echo "===== MultiCategory is running in port 8090 ====="
echo "================================================="