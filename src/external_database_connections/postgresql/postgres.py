"""
Information to query schemata of the database:

\dt -- returns a list of tables in the database

-- returns a list of attributes in the selected table
SELECT column_name 
FROM information_schema.columns 
WHERE table_name = 'actor' 
ORDER BY ordinal_position;

"""

import psycopg2
import psycopg2.extras
from external_database_connections.config.config import config


class Postgres():

    def __init__(self, name, section="postgresql"):
        self.name = name
        self.conn = None
        self.primary_keys = None
        try:
            params = config(section=section)
            #print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(**params)
            self.primary_keys = self.get_primary_keys()
            self.table_names = self.get_table_names()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_name(self):
        return self.name

    def query(self, query="SELECT version()"):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(query)
        ## This returns list of tuples because the cursor_factory was defined with DictCursor
        rows = cur.fetchall()
        #print("The number of rows: ", cur.rowcount)
        # for row in rows:
        #     print(row)
        cur.close()
        return rows

    def close(self):
        if self.conn is not None:
            self.conn.close()
            print('Database connection closed.')

    def get_table_names(self):
        result = []
        table_names = self.query(
            "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';")
        for name_tuple in table_names:
            result.append(name_tuple[0])
        return result

    def get_attributes_for_table(self, table_name):
        result = list()
        query = "SELECT column_name FROM information_schema.columns WHERE table_name = '" + \
            table_name + "' ORDER BY ordinal_position;"
        attributes = self.query(query)
        for attribute in attributes:
            print(attribute)
            result.append(attribute[0])
        return result

    def get_schema(self):
        result = dict()
        for name in self.table_names:
            result[name] = self.get_attributes_for_table(name)
        print(result)
        return result

    def get_primary_keys(self):
        query = """ 
                SELECT kcu.table_schema,
                    kcu.table_name,
                    tco.constraint_name,
                    kcu.ordinal_position as position,
                    kcu.column_name as key_column
            FROM information_schema.table_constraints tco
            JOIN information_schema.key_column_usage kcu 
                    on kcu.constraint_name = tco.constraint_name
                    and kcu.constraint_schema = tco.constraint_schema
                    and kcu.constraint_name = tco.constraint_name
            WHERE tco.constraint_type = 'PRIMARY KEY'
            ORDER BY kcu.table_schema,
                kcu.table_name,
                position;"""
        result = self.query(query)
        tables_keys = dict()
        for elem in result:
            tables_keys[elem[1]] = elem[4]
        return tables_keys

    def get_foreign_keys_for_table(self, table_name):
        query = """
                SELECT
            tc.table_schema, 
            tc.constraint_name, 
            tc.table_name, 
            kcu.column_name, 
            ccu.table_schema AS foreign_table_schema,
            ccu.table_name AS foreign_table_name,
            ccu.column_name AS foreign_column_name 
        FROM 
            information_schema.table_constraints AS tc 
            JOIN information_schema.key_column_usage AS kcu
            ON tc.constraint_name = kcu.constraint_name
            AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage AS ccu
            ON ccu.constraint_name = tc.constraint_name
            AND ccu.table_schema = tc.table_schema
        WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name='""" + table_name + "';"
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
        query = """SELECT 
                    tc.table_name, 
                    kcu.column_name,
                    ccu.table_name AS foreign_table_name,
                    ccu.column_name AS foreign_column_name 
                FROM 
                    information_schema.table_constraints AS tc 
                    JOIN information_schema.key_column_usage AS kcu
                    ON tc.constraint_name = kcu.constraint_name
                    AND tc.table_schema = kcu.table_schema
                    JOIN information_schema.constraint_column_usage AS ccu
                    ON ccu.constraint_name = tc.constraint_name
                    AND ccu.table_schema = tc.table_schema
                WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name='""" + table_name + "';"
        return self.query(query)

    def get_edge_schema_for_tables(self):
        result = dict()
        table_names = self.get_table_names()
        for table_name in table_names:
            info = self.query_edge_schema_for_table(table_name)
            result[table_name] = info
        return result

    def get_column_datatypes_for_table(self, table):
        query = """
        select column_name, data_type from information_schema.columns where table_name = '""" + table + "';"
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
        """ Connect to the PostgreSQL database server """
        try:
            params = config()
            print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(**params)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
