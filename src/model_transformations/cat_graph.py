from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import FOAF , XSD
from external_database_connections.postgresql.postgres import Postgres
from external_database_connections.neo4j.neo4j import Neo4j

"""
https://www.w3.org/TR/rdf11-concepts/

An RDF triple consists of three components:

    - the subject, which is an IRI or a blank node
    - the predicate, which is an IRI
    - the object, which is an IRI, a literal or a blank node
"""

class CatGraph():

    def __init__(self, name, database):
        self.name = name
        self.graph = Graph()
        self.database = database

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
        self.transform_tables()
        #edge_schema = self.database.get_edge_schema_for_tables()
        #print(edge_schema)

    def transform_tables(self):
        table_names = self.database.get_table_names()
        primary_keys = self.database.get_primary_keys()
        for table in table_names:
            table_result = self.database.query("SELECT * FROM " + table + ";")
            table_schema = self.database.get_attributes_for_table(table)
            try:
                self.transform_table(table, primary_keys[table], table_schema, table_result)
            except KeyError:
                print("Table " + table + " is not in the primary key dictionary. This is passed.")
                pass

    def transform_table(self, table_name, primary_key, table_schema, table_result):
        database_name = self.database.get_name()
        for row in table_result:
            central_iri = URIRef(database_name + "/" + table_name + "/" + primary_key + "/" + str(row[primary_key]))
            for attr in table_schema:
                if attr != primary_key:
                    edge_iri = URIRef(database_name + "/" + table_name + "/" + primary_key + "/" + str(attr))
                    target_literal = Literal(row[attr])
                    triple = (central_iri, edge_iri, target_literal)
                    self.graph.add(triple)

    def transform_from_property_graph(self):
        return None