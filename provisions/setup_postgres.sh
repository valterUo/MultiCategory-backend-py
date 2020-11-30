#!/bin/bash

echo
echo "======================================================="
echo "===== Creating PostgreSQL database with LDBC data ====="
echo "======================================================="

docker pull postgres
docker run -d -h multicategory-postgres --net=multicategory -p5400:5400 -p8080:8080 -e "PGPORT=5400" -e "BDHOST=multicategory-postgres" -e POSTGRES_PASSWORD=0000 --name multicategory-postgres postgres
docker cp dbsetup multicategory-postgres:/
docker exec multicategory-postgres apt-get update
docker exec multicategory-postgres apt-get install curl -y
docker exec multicategory-postgres apt-get install dos2unix -y
docker exec multicategory-postgres dos2unix dbsetup/postgres/ldbc/load.sh
docker exec multicategory-postgres bash dbsetup/postgres/ldbc/load.sh