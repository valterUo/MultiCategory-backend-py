from abstract_category.functor.functor import Functor
from external_database_connections.neo4j.neo4j import Neo4j
from external_database_connections.postgresql.postgres import Postgres
from model_transformations.data_transformations.data_transformation import Transformation

db = Postgres("ldbcsf1")

graph_db = Neo4j("testdb")

f = Functor("test", {"objects": ["person", "knows"], "morphisms": [{"source": "knows", "morphism": ("k_person1id", "p_personid"), "target": "person"}, {"source": "knows", "morphism": (
    "k_person2id", "p_personid"), "target": "person"}]}, {"person": "nodes", "knows": "edges", ("k_person1id", "p_personid"): "source", ("k_person2id", "p_personid"): "target"},
    {"objects": ["nodes", "edges"], "morphisms": [{"source": "edges", "morphism": "source", "target": "nodes"}, {"source": "edges", "morphism": "target", "target": "nodes"}]})

tr = Transformation(db, graph_db, f)
