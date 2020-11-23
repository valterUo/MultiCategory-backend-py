import psycopg2
import psycopg2.extras
from external_database_connections.config.config import config
import json
import os
dirname = os.path.dirname(__file__)
examples_path = os.path.join(dirname, "schemaQueries.json")

class Postgres():

    def __init__(self, name, section="postgresql"):
        self.name = name
        self.conn = None
        self.primary_keys = None
        with open(examples_path) as queries:
            self.schema_queries = json.load(queries)
        try:
            params = config(section=section)
            #print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(**params)
            self.table_names = self.get_table_names()
            self.primary_keys = self.get_primary_keys()
            self.all_pk_fk_contrainsts = self.get_all_pk_fk_contrainsts()
            self.foreign_keys = self.all_pk_fk_contrainsts.values()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_name(self):
        return self.name

    def __str__(self):
        return "PostgreSQL " + self.name

    def connected(self):
        return self.conn != None

    def contains_table(self, table):
        return table in self.table_names

    def is_primary_key(self, key):
        return key in self.primary_keys.values()

    def is_foreign_key(self, key):
        return key in self.foreign_keys

    def return_all_pk_fk_contrainsts(self):
        return self.all_pk_fk_contrainsts

    def query(self, query="SELECT version()", mode="list",):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(query)
        ## This returns list of tuples because the cursor_factory was defined with DictCursor
        if mode == "dict":
            rows = [dict(record) for record in cur]
        else:
            rows = cur.fetchall()
        cur.close()
        return rows

    def close(self):
        if self.conn is not None:
            self.conn.close()
            print('Database connection closed.')

    def get_table_names(self):
        result = []
        query = self.schema_queries["tableNames"]
        table_names = self.query(query)
        for name_tuple in table_names:
            result.append(name_tuple[0])
        return result

    def get_attributes_for_table(self, table_name):
        result = list()
        query = "SELECT column_name FROM information_schema.columns WHERE table_name = '" + \
            table_name + "' ORDER BY ordinal_position;"
        attributes = self.query(query)
        for attribute in attributes:
            result.append(attribute[0])
        return result

    def get_table_for_attribute(self, attribute):
        schema = self.get_schema()
        attribute = attribute.strip()
        for table in schema:
            for table_attr in schema[table]:
                if attribute == table_attr:
                    return table
        return None

    def get_schema(self):
        result = dict()
        for name in self.table_names:
            result[name] = self.get_attributes_for_table(name)
        return result

    def get_primary_keys(self):
        query = self.schema_queries["primaryKeys"]
        result = self.query(query)
        tables_keys = dict()
        for elem in result:
            tables_keys[elem[1]] = elem[4]
        return tables_keys

    def get_foreign_keys_for_table(self, table_name):
        query = self.schema_queries["foreignKeysForTable"] + "'" + table_name + "';"
        result = self.query(query)
        tables_foreign_keys = dict()
        for elem in result:
            connection = dict()
            connection["foreign_key"] = elem[3]
            connection["target_table"] = elem[5]
            connection["primary_key_in_target_table"] = elem[6]
            tables_foreign_keys[elem[3]] = connection
        return tables_foreign_keys

    def get_all_pk_fk_contrainsts(self):
        result = dict()
        for table in self.table_names:
            result[table] = self.get_foreign_keys_for_table(table)
        return result

    def get_primary_key(self, table_name):
        if self.primary_keys != None:
            try:
                return self.primary_keys[table_name]
            except:
                print("Table not in the database")

    def query_edge_schema_for_table(self, table_name):
        query = self.schema_queries["edgeSchemaForTable"] + "'" + table_name + "';"
        return self.query(query)

    def get_edge_schema_for_tables(self):
        result = dict()
        table_names = self.get_table_names()
        for table_name in table_names:
            info = self.query_edge_schema_for_table(table_name)
            result[table_name] = info
        return result

    def get_column_datatypes_for_table(self, table_name):
        query = self.schema_queries["columnDatatypesForTable"] + "'" + table_name + "';"
        result = self.query(query)
        columns_datatypes = dict()
        for elem in result:
            columns_datatypes[elem[0]] = elem[1]
        return columns_datatypes

    def get_all_columns_datatypes(self):
        result = dict()
        for table in self.table_names:
            result.update(self.get_column_datatypes_for_table(table))
        return result

    def connect(self):
        try:
            params = config()
            print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(**params)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
