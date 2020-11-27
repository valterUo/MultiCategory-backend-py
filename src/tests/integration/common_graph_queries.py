from external_database_connections.neo4j.neo4j import Neo4j
from external_database_connections.postgresql.postgres import Postgres
from abstract_category.functor.functor import Functor
from model_transformations.data_transformations.rel_to_graph_data_transformation import RelToGraphDataTransformation
from tests.integration.tested_functors import tested_functors

def general_setup(selected_functor):
    graph_db = Neo4j("ldbcsf1")
    graph_db.empty_database()
    rel_db = Postgres("ldbcsf1")
    functors = tested_functors()
    functor_def = functors[selected_functor]
    functor = Functor("test", functor_def)
    tr = RelToGraphDataTransformation(rel_db, graph_db, functor)
    tr.transform()

def count_nodes(graph_db):
    graph_query = 'MATCH (p) RETURN count(p)'
    res = graph_db.execute_read(graph_query)
    return res[0]["count(p)"]

def count_edges(graph_db, edge_label):
    graph_query = 'MATCH p=()-[r:' + edge_label + ']->() RETURN count(p)'
    res = graph_db.execute_read(graph_query)
    return res[0]["count(p)"]