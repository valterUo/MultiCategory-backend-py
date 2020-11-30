#!/bin/bash

echo
echo "==============================="
echo "===== Starting PostgreSQL ====="
echo "==============================="

docker start multicategory-postgres

echo
echo "==============================="
echo "======= Starting Neo4j ========"
echo "==============================="

docker start multicategory-neo4j

echo
echo "=================================="
echo "===== Starting MultiCategory ====="
echo "=================================="

if docker start multicategory-running ; then
    echo "MultiCategory running in localhost:8090"
else 
    docker run -it --publish 8090:8050 --detach --rm --net=multicategory --name multicategory-running multicategory
    echo "MultiCategory running in localhost:8090"
fi
