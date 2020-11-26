import json
import unittest
import os

from external_database_connections.postgresql.postgres import Postgres
from external_database_connections.neo4j.neo4j import Neo4j
from model_transformations.data_transformations.rel_to_graph_data_transformation import RelToGraphDataTransformation
from abstract_category.functor.functor import Functor

dirname = os.path.dirname(__file__)
rel_db = Postgres("ldbcsf1")
graph_db = Neo4j("ldbcsf1")

test_cases = dict()
test_file_path = os.path.join(dirname, "tested_functors.json")
with open(test_file_path, 'r') as reader:
    functors = json.load(reader)

print(functors)

class TestRelToGraphDataTransformation(unittest.TestCase):

    def test_data_transformation1(self):
        pass
        # graph_db.empty_database()
        # functor_def = functors["test1"]
        # functor = Functor(functor_def)
        # tr = RelToGraphDataTransformation(rel_db, graph_db, functor)
        # tr.transform()
        # graph_query = 'MATCH p=(n)-[r:k_person2id_k_person1id]->(m) WHERE n.p_firstname = "Carmen" AND n.p_lastname = "Lepland" RETURN p LIMIT 25'
        # graph_db.execute_read(graph_query)