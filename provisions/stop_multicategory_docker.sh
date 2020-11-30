#!/bin/bash

echo
echo "==============================="
echo "===== Stopping PostgreSQL ====="
echo "==============================="

docker stop multicategory-postgres

echo
echo "=========================="
echo "===== Stopping Neo4j ====="
echo "=========================="


docker stop multicategory-neo4j

echo
echo "=================================="
echo "===== Stopping MultiCategory ====="
echo "=================================="

docker stop multicategory-running