#!/bin/bash

echo
echo "==============="
echo "=== Starting =="
echo "==============="

if [-d "ldbc_flatfiles"]; then
       echo "The ldbc_flatfiles folder already exists"
else
       curl -o ldbc_flatfiles.tar.gz --create-dirs --location --remote-header-name --remote-name "https://github.com/valterUo/multicategory-flatfiles/raw/main/ldbc_flatfiles.tar.gz"
       tar xvzf ldbc_flatfiles.tar.gz
fi

echo
echo "========================================="
echo "===== Creating the ldbcsf1 database ====="
echo "========================================="

psql -c "DROP DATABASE IF EXISTS ldbcsf1" -U postgres
psql -c "CREATE DATABASE ldbcsf1" -U postgres

echo
echo "==========================="
echo "===== Creating schema ====="
echo "==========================="

psql -f schema.sql -d ldbcsf1 -U postgres

echo
echo "========================================="
echo "===== Creating schema constraints ======="
echo "========================================="

psql -f schema_constraints.sql -d ldbcsf1 -U postgres

echo
echo "=================================================="
echo "===== Uploading data from ldbcsf1 flat files ====="
echo "=================================================="

psql -f snb-load.sql -d ldbcsf1 -U postgres

psql -c "\copy forum FROM 'ldbc_flatfiles/forum_0_0.csv' WITH DELIMITER '|' CSV HEADER;" -d ldbcsf1 -U postgres

echo
echo "================="
echo "===== Done. ====="
echo "================="