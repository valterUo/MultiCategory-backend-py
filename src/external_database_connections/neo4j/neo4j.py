from external_database_connections.config.config import config
from neo4j import GraphDatabase
from neo4j.exceptions import ClientError
from external_database_connections.neo4j.help_functions import formulate_set_string, fix_dictionary


class Neo4j:

    def __init__(self, name, section="neo4j"):
        self.name = name
        self.driver = None
        self.labels = []
        try:
            params = config(section=section)
            uri = params["uri"]
            auth = (params["user"], params["password"])
            self.driver = GraphDatabase.driver(uri=uri, auth=auth)
            result = self.execute_read("MATCH (n) RETURN distinct labels(n)")
            for record in result:
                self.labels.append(record["labels(n)"])
        except Exception as error:
            print(error)
            print("Neo4j is not running!")

    def get_name(self):
        return self.name

    def __str__(self):
        return "Neo4j " + self.name

    def connected(self):
        return self.driver != None

    def close(self):
        self.driver.close()

    def is_empty(self):
        query = "MATCH (n) RETURN count(n)"
        res = self.execute_read(query)
        return res[0]["count(n)"] == 0

    def execute_write(self, query):
        with self.driver.session() as session:
            node = session.write_transaction(self._execute_query, query)
            return node

    def execute_read(self, query):
        with self.driver.session() as session:
            node = session.read_transaction(self._execute_query, query)
            return node

    def empty_database(self):
        query = "MATCH (n) DETACH DELETE n"
        result = self.execute_write(query)
        #print(result)

    def create_and_return_node(self, property_name, attributes):
        with self.driver.session() as session:
            node = session.write_transaction(
                self._create_and_return_node, property_name, attributes)

    def create_index(self, rel_db, table_name, recalculate=False):
        primary_key = rel_db.get_primary_key(table_name)
        primary_key_index_query = "CREATE INDEX " + table_name + \
            "_primary_key_index " + \
            " FOR (n:" + table_name + ") ON (n." + primary_key + ")"
        drop_index = "DROP INDEX " + table_name + "_primary_key_index"
        try:
            self.execute_write(primary_key_index_query)
        except ClientError:
            if recalculate:
                print("Index exists. Index is recalculated.")
                self.execute_write(drop_index)
                self.execute_write(primary_key_index_query)
            else:
                print("Index exists. Index is not recalculated.")

    def transform_table_into_collection_of_nodes(self, rel_db, table_name):
        self.create_index(rel_db, table_name, True)
        result = rel_db.query("SELECT * FROM " + table_name + ";")
        for result_dict in result:
            d = dict(result_dict)
            self.create_and_return_node(table_name, d)

    def transform_tables_into_graph_db(self, rel_db):
        rel_schema = rel_db.get_schema()
        for table_name in rel_schema:
            self.transform_table_into_collection_of_nodes(rel_db, table_name)
        result = self.execute_read("MATCH (n) RETURN distinct labels(n)")
        for record in result:
            self.labels.append(record["labels(n)"])

    def create_edges(self, rel_db):
        for table in rel_db.get_table_names():
            print(table)
            for key_foreign_key_pair in rel_db.query_edge_schema_for_table(table):
                print(key_foreign_key_pair)
                label1 = key_foreign_key_pair[0]
                foreign_key = key_foreign_key_pair[1]
                label2 = key_foreign_key_pair[2]
                primary_key = key_foreign_key_pair[3]
                self.create_edges_between_two_collections_of_nodes(
                    label1, foreign_key, primary_key, label2)

    def create_edges_between_two_collections_of_nodes(self, label1, foreign_key, primary_key, label2):
        query = """
            MATCH (a: """ + label1 + """)
            MATCH (b: """ + label2 + """)
            WHERE a.""" + foreign_key + """ = b.""" + primary_key + """
            CREATE (a)-[r:""" + foreign_key + """_""" + primary_key + """]->(b);
        """
        self.execute_write(query)

    @staticmethod
    def _create_and_return_node(tx, property_name, value_dict):
        set_string = formulate_set_string(value_dict)
        try:
            result = tx.run("CREATE (a:" + property_name +
                            ") " + set_string, **value_dict)
        except TypeError as err:
            print(str(err))
            print("Type error: {0}".format(err))
            value_dict = fix_dictionary(value_dict)
            set_string = formulate_set_string(value_dict)
            result = tx.run("CREATE (a:" + property_name +
                            ") " + set_string, **value_dict)
        return result.single()[0]

    @staticmethod
    def _execute_query(tx, query):
        result2 = []
        result = tx.run(query)
        for record in result:
            result2.append(record)
        return result2
