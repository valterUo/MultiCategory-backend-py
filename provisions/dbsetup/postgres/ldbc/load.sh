#!/bin/bash

this_dir=`dirname $0`

echo
echo "==============="
echo "=== Starting =="
echo "==============="

if [ -f "$this_dir/ldbc_flatfiles.tar.gz"]; then
       echo "The ldbc_flatfiles folder already exists"
else
       curl -o ldbc_flatfiles.tar.gz --create-dirs --location --remote-header-name --remote-name "https://github.com/valterUo/multicategory-flatfiles/raw/main/ldbc_flatfiles.tar.gz"
       tar xvzf ldbc_flatfiles.tar.gz
fi

echo
echo "========================================="
echo "===== Creating the ldbcsf1 database ====="
echo "========================================="

psql -c "DROP DATABASE IF EXISTS ldbcsf1 WITH (FORCE);" -U postgres
psql -c "CREATE DATABASE ldbcsf1;" -U postgres

echo
echo "==========================="
echo "===== Creating schema ====="
echo "==========================="

psql -f $this_dir/schema.sql -d ldbcsf1 -U postgres

echo
echo "========================================="
echo "===== Creating schema constraints ======="
echo "========================================="

psql -f $this_dir/schema_constraints.sql -d ldbcsf1 -U postgres
psql -f $this_dir/foreign_key_constraints.sql -d ldbcsf1 -U postgres


echo
echo "=================================================="
echo "===== Uploading data from ldbcsf1 flat files ====="
echo "=================================================="

psql -f $this_dir/snb-load.sql -d ldbcsf1 -U postgres

echo
echo "============================================="
echo "===== ldbcsf1 database has been created ====="
echo "============================================="