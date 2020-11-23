#!/bin/bash

# This script does the following:
# 	- Docker initialization: creates the "multicategory" docker network if not already created
# 	- Image pull: pulls Postgres and Neo4j base images from dockerhub
# 	- Container run: runs the above containers
# 	- Data preparation: download and insert data into running containers

./cleanup_containers.sh

echo
echo "===================================================================="
echo "===== Creating the multicategory docker network if not present ====="
echo "===================================================================="
$(docker network inspect multicategory &>/dev/null) || {   docker network create multicategory; }

echo
echo "========================================"
echo "===== Pulling images from Dockerhub====="
echo "========================================"
docker pull neo4j
docker pull postgres

echo
echo "============================="
echo "===== Running containers====="
echo "============================="
docker run -d -h multicategory-postgres --net=multicategory -p 5400:5400 -p 8080:8080 -e "PGPORT=5400" -e "BDHOST=multicategory-postgres" --name multicategory-postgres postgres
docker run -d -h multicategory-neo4j --net=multicategory -p 5401:5401 -e "PGPORT=5401" -e "BDHOST=multicategory-neo4j" --name multicategory-neo4j neo4j


echo
echo "========================"
echo "===== Loading data ====="
echo "========================"

# # Download the mimic2 dataset
# if [ -f "mimic2_flatfiles.tar.gz" ]
# then
#        echo "Mimic data already exists. Skipping download"
# else
#        echo "Downloading the mimic2 dataset"
#        curl -o mimic2_flatfiles.tar.gz --create-dirs https://archive.physionet.org/mimic2/demo/mimic2_flatfiles.tar.gz
# fi

# # Download mimic2 waveform data
# if [ -f "a40001_000001.dat" ]
# then
#        echo "Mimic waveform data already exists. Skipping download"
# else
#        echo "Downloading the mimic2 waveform data"
#        curl -o a40001_000001.dat --create-dirs https://physionet.org/physiobank/database/mimic2db/a40001/a40001_000001.dat
#        curl -o a40001_000001.hea --create-dirs https://physionet.org/physiobank/database/mimic2db/a40001/a40001_000001.hea
# fi

# # Download mimic2 logs
# # https://physionet.org/physiobank/database/mimic2cdb-ps/
# if [ -f "s00318.txt" ]
# then
#        echo "Mimic log data already exists. Skipping download"
# else
#        echo "Downloading the mimic2 log data"
#        curl -o s00318.txt --create-dirs https://physionet.org/physiobank/database/mimic2cdb-ps/s00318/s00318.txt
# fi

# # postgres-catalog
# docker exec -u root bigdawg-postgres-catalog mkdir -p /src/main/resources
# docker cp ../src/main/resources/PostgresParserTerms.csv bigdawg-postgres-catalog:/src/main/resources
# docker cp ../src/main/resources/SciDBParserTerms.csv bigdawg-postgres-catalog:/src/main/resources
# docker cp cluster_setup/postgres-catalog/bdsetup bigdawg-postgres-catalog:/
# docker exec bigdawg-postgres-catalog /bdsetup/setup.sh

# # postgres-data1
# docker cp cluster_setup/postgres-data1/bdsetup bigdawg-postgres-data1:/
# docker cp mimic2_flatfiles.tar.gz bigdawg-postgres-data1:/bdsetup/
# docker exec --user=root bigdawg-postgres-data1 /bdsetup/setup.sh

# # postgres-data2
# docker cp cluster_setup/postgres-data2/bdsetup bigdawg-postgres-data2:/
# docker cp mimic2_flatfiles.tar.gz bigdawg-postgres-data2:/bdsetup/
# docker exec --user=root bigdawg-postgres-data2 /bdsetup/setup.sh

# # scidb
# docker cp cluster_setup/scidb-data/bdsetup bigdawg-scidb-data:/home/scidb/
# docker cp a40001_000001.dat bigdawg-scidb-data:/home/scidb/bdsetup
# docker cp a40001_000001.hea bigdawg-scidb-data:/home/scidb/bdsetup
# docker exec bigdawg-scidb-data /home/scidb/bdsetup/setup.sh

# # accumulo
# docker cp cluster_setup/accumulo-data/bdsetup bigdawg-accumulo-zookeeper:/
# docker cp s00318.txt bigdawg-accumulo-zookeeper:/bdsetup/
# docker exec bigdawg-accumulo-zookeeper python /bdsetup/setup.py

echo
echo "======================================="
echo "===== Starting BigDAWG Middleware ====="
echo "======================================="
# docker exec -d bigdawg-scidb-data java -classpath "istc.bigdawg-1.0-SNAPSHOT-jar-with-dependencies.jar" istc.bigdawg.Main bigdawg-scidb-data
# docker exec -d bigdawg-accumulo-zookeeper java -classpath "istc.bigdawg-1.0-SNAPSHOT-jar-with-dependencies.jar" istc.bigdawg.Main bigdawg-accumulo-zookeeper
# docker exec -d bigdawg-postgres-data1 java -classpath "istc.bigdawg-1.0-SNAPSHOT-jar-with-dependencies.jar" istc.bigdawg.Main bigdawg-postgres-data1
# docker exec -d bigdawg-postgres-data2 java -classpath "istc.bigdawg-1.0-SNAPSHOT-jar-with-dependencies.jar" istc.bigdawg.Main bigdawg-postgres-data2
# docker exec -it bigdawg-postgres-catalog java -classpath "istc.bigdawg-1.0-SNAPSHOT-jar-with-dependencies.jar" istc.bigdawg.Main bigdawg-postgres-catalog

echo
echo "================="
echo "===== Done. ====="
echo "================="