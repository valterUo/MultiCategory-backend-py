#!/bin/bash

echo
echo "==================================================================="
echo "===== multicategory-postgres: Stopping and removing container ====="
echo "==================================================================="

docker rm -f multicategory-postgres

echo
echo "================================================================"
echo "===== multicategory-neo4j: Stopping and removing container ====="
echo "================================================================"

docker rm -f multicategory-neo4j

echo
echo "=========================================================================="
echo "===== Done. Final container status (both running and stopped state): ====="
echo "=========================================================================="

docker ps -a