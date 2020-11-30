#!/bin/bash

# This script does the following:
#   - Removes the containers if they already exists
# 	- Docker initialization: creates the "multicategory" docker network if not already created
# 	- Image pull: pulls Postgres and Neo4j base images from dockerhub and keeps them updated
# 	- Container run: runs the above containers
# 	- Data preparation: download and insert data into running containers (Postgres only)

./cleanup_containers.sh

echo
echo "===================================================================="
echo "===== Creating the multicategory docker network if not present ====="
echo "===================================================================="
$(docker network inspect multicategory &>/dev/null) || {   docker network create multicategory; }

echo
echo "========================================="
echo "===== Pulling images from Dockerhub ====="
echo "========================================="

./setup_postgres.sh
./setup_neo4j.sh
./setup_multicategory.sh

echo
echo "===================================="
echo "==== The installation is done ====="
echo "===================================="
echo
echo "Use stop_multicategory.sh to stop the system safely"
echo "Use start_multicategory_docker.sh to start the system without repeating the installation"