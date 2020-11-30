#!/bin/bash

echo
echo "========================================="
echo "===== Creating empty Neo4j database ====="
echo "========================================="

docker pull neo4j
docker run -d --net=multicategory -p7474:7474 -p7687:7687 -e NEO4J_AUTH=neo4j/0000 --name multicategory-neo4j neo4j