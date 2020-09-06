from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import FOAF, XSD
from external_database_connections.postgresql.postgres import Postgres
from external_database_connections.neo4j.neo4j import Neo4j
from rdflib import plugin
from rdflib.store import Store
from rdflib_sqlalchemy import registerplugins

"""
https://www.w3.org/TR/rdf11-concepts/

An RDF triple consists of three components:

    - the subject, which is an IRI or a blank node
    - the predicate, which is an IRI
    - the object, which is an IRI, a literal or a blank node
"""


class CatGraph():

    def __init__(self, name, database, rdf_database_uri, persistent=True):
        registerplugins()
        self.rdf_database_uri = "postgresql+psycopg2://postgres:0000@localhost:5432/catGraph"
        self.name = name
        self.database = database
        if persistent:
            store = plugin.get("SQLAlchemy", Store)(
                identifier="cat_graph_test")
            self.graph = Graph(store, identifier="cat_graph_test")
            self.graph.open(self.rdf_database_uri, create=True)
        else:
            self.graph = Graph()

    def get_name(self):
        return self.name

    def get_cat_graph(self):
        return self.graph

    def get_database(self):
        return self.database

    def transform_from(self):
        if type(self.database) == Postgres:
            self.transform_from_relational()
        elif type(self.database) == Neo4j:
            self.transform_from_property_graph()

    def transform_from_relational(self):
        if len(self.graph) == 0:
            self.transform_tables()
            self.transform_key_foreign_key_pairs()
        else:
            print("The graph is not empty.")

    def transform_tables(self):
        table_names = self.database.get_table_names()
        primary_keys = self.database.get_primary_keys()
        for table in table_names:
            table_result = self.database.query("SELECT * FROM " + table + ";")
            table_schema = self.database.get_attributes_for_table(table)
            try:
                self.transform_table(
                    table, primary_keys[table], table_schema, table_result)
            except KeyError:
                print("Table " + table +
                      " is not in the primary key dictionary. This is passed.")
                pass

    def transform_table(self, table_name, primary_key, table_schema, table_result):
        database_name = self.database.get_name()
        for row in table_result:
            central_iri = URIRef(database_name + "/" + table_name +
                                 "/" + primary_key + "/" + str(row[primary_key]))
            for attr in table_schema:
                if attr != primary_key:
                    edge_iri = URIRef(
                        database_name + "/" + table_name + "/" + primary_key + "/" + str(attr))
                    target_literal = Literal(row[attr])
                    triple = (central_iri, edge_iri, target_literal)
                    self.graph.add(triple)

    def transform_key_foreign_key_pairs(self):
        ## 'store': [['store', 'address_id', 'address', 'address_id'], ['store', 'manager_staff_id', 'staff', 'staff_id']], 'address': [['address', 'city_id', 'city', 'city_id']]
        edge_schema = self.database.get_edge_schema_for_tables()
        database_name = self.database.get_name()
        ## For table we might have zero or multiple foreign keys
        for table_name in edge_schema:
            print(table_name)
            if len(edge_schema[table_name]) != 0:
                list_of_keys = edge_schema[table_name]
                for key_info in list_of_keys:
                    ## For example, ['store', 'address_id', 'address', 'address_id']
                    primary_key = key_info[3]
                    foreign_key = key_info[1]
                    main_table = key_info[2]
                    result_list_of_lists = self.database.query("SELECT a." + primary_key + ", b." + foreign_key + " from " +
                                                               key_info[2] + " AS a JOIN " + key_info[0] + " AS b ON a." + primary_key + "= b." + foreign_key + ";")
                    for result in result_list_of_lists:
                        subject = URIRef(
                            database_name + "/" + table_name + "/" + foreign_key + "/" + str(result[0]))
                        predicate = URIRef(database_name + "/" + table_name +
                                           "/" + foreign_key + "/" + main_table + "/" + primary_key)
                        object_elem = URIRef(
                            database_name + "/" + table_name + "/" + primary_key + "/" + str(result[1]))
                        self.graph.add((subject, predicate, object_elem))

    def transform_node(self, node):
        database_name = self.database.get_name()
        labels = node.labels
        label_path = ""
        for label in labels:
            label_path = label_path + "/" + str(label)
        id_value = node.id
        central_subject = URIRef(
            database_name + label_path + "/" + str(id_value))
        for prop in node.keys():
            edge_iri = URIRef(database_name + label_path + "/" + str(prop))
            target_literal = Literal(str(node[prop]))
            triple = (central_subject, edge_iri, target_literal)
            self.graph.add(triple)
        return central_subject

    def transform_edge(self, source_uri, edge, target_uri):
        database_name = self.database.get_name()
        id_value = edge.id
        properties = edge.values()
        central_subject = URIRef(database_name + "/edge/" + str(id_value))
        for prop in properties:
            edge_iri = URIRef(database_name + "/edge/" + str(prop))
            target_literal = Literal(str(properties[prop]))
            triple = (central_subject, edge_iri, target_literal)
            self.graph.add(triple)
        source = URIRef(database_name + "/source/")
        self.graph.add((source_uri, source, central_subject))
        target = URIRef(database_name + "/target/")
        self.graph.add((central_subject, target, target_uri))

    def transform_from_property_graph(self):
        result = self.database.execute_read(
            "MATCH (n) -[r]-> (m) RETURN n, r, m")
        for elem in result:
            source = self.transform_node(elem["n"])
            target = self.transform_node(elem["m"])
            self.transform_edge(source, elem["r"], target)
