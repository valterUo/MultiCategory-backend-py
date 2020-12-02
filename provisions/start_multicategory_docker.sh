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
echo "Waiting Neo4j to start"
sleep 10

echo
echo "=================================="
echo "===== Starting MultiCategory ====="
echo "=================================="

if docker start multicategory-running ; then
    echo "MultiCategory running in localhost:8090"
else 
    docker run -it --publish 8090:8050 --detach --net=multicategory --name multicategory-running multicategory
    echo "MultiCategory running in localhost:8090"
fi
