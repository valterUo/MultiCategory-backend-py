from external_database_connections.config.config import config
from neo4j import GraphDatabase
from neo4j.exceptions import ClientError
from external_database_connections.neo4j.help_functions import formulate_set_string, fix_dictionary


class Neo4j:

    def __init__(self, section="neo4j"):
        params = config(section=section)
        uri = params["uri"]
        auth = (params["user"], params["password"])
        self.driver = GraphDatabase.driver(uri=uri, auth=auth)
        self.labels = self.execute("MATCH (n) RETURN distinct labels(n)")

    def close(self):
        self.driver.close()

    def create_and_return_node(self, property_name, attributes):
        with self.driver.session() as session:
            node = session.write_transaction(
                self._create_and_return_node, property_name, attributes)
            #print(node)

    def execute(self, query):
        with self.driver.session() as session:
            node = session.write_transaction(self._execute_query, query)
            return node

    def empty_database(self):
        query = "MATCH (n) DETACH DELETE n"
        result = self.execute(query)
        #print(result)

    def create_index(self, rel_db, table_name, recalculate=False):
        primary_key = rel_db.get_primary_key(table_name)
        primary_key_index_query = "CREATE INDEX " + table_name + \
            "_primary_key_index " + \
            " FOR (n:" + table_name + ") ON (n." + primary_key + ")"
        drop_index = "DROP INDEX " + table_name + "_primary_key_index"
        try:
            self.execute(primary_key_index_query)
        except ClientError:
            if recalculate:
                print("Index exists. Index is recalculated.")
                self.execute(drop_index)
                self.execute(primary_key_index_query)
            else:
                print("Index exists. Index is not recalculated.")

    def transform_tables_into_graph_db(self, rel_db):
        rel_schema = rel_db.get_schema()
        for table_name in rel_schema:
            self.transform_table_into_collection_of_nodes(rel_db, table_name)
        self.labels = self.execute("MATCH (n) RETURN distinct labels(n)")
        print(self.labels)

    def transform_table_into_collection_of_nodes(self, rel_db, table_name):
        self.create_index(rel_db, table_name, True)
        result = rel_db.query("SELECT * FROM " + table_name + ";")
        #print(result)
        for result_dict in result:
            d = dict(result_dict)
            self.create_and_return_node(table_name, d)

    def create_collection_of_nodes(self, property_name, attributes_values):
        for elem in attributes_values:
            self.create_and_return_node(property_name, attributes_values)

    def create_edges_from_foreign_key_to_primary_key(self, rel_db):
        edge_schema = rel_db.query_edge_schema_for_table()

    def create_edges(self, rel_db):
        for table in rel_db.get_table_names():
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
        self.execute(query)

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
        result = tx.run(query)
        return result