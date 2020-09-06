#from initialization_of_demo_databases.initialize_ecommerce import ECommerceMultiModelDatabase
#from initialization_of_demo_databases.initialize_patent_data import PatentMultiModelDatabase
#from supportive_functions.row_manipulations import find_values_from_tree
#from supportive_functions.compositions import tree_to_nx_graph
import networkx as nx
import matplotlib.pyplot as plt
#from supportive_functions.compositions import compose_lambda_functions
from external_database_connections.postgresql.postgres import Postgres
from external_database_connections.neo4j.neo4j import Neo4j
from model_transformations.cat_graph import CatGraph

dvdrental_relational_to_rdf_uri = "postgresql+psycopg2://postgres:0000@localhost:5432/catGraph"
dvdrental_property_graph_to_rdf_uri = "postgresql+psycopg2://postgres:0000@localhost:5432/catGraph2"

#patent_db = PatentMultiModelDatabase()
#ecommerce_db = ECommerceMultiModelDatabase()

#db = Postgres("dvdrental")
graph_db = Neo4j("dvdrental")

# catgraph = CatGraph("test_graph", db, dvdrental_relational_to_rdf_uri)
# catgraph.transform_from()
# g = catgraph.get_cat_graph()

# # i = 0
# # for subj, pred, obj in g:
# #     i+=1
# #     if i % 10000 == 0:
# #         print(subj, pred, obj)

# print("graph has {} statements.".format(len(g)))

catgraph = CatGraph("test_graph2", graph_db, dvdrental_property_graph_to_rdf_uri)
catgraph.transform_from()
g = catgraph.get_cat_graph()

i = 0
for subj, pred, obj in g:
    i+=1
    if i % 1000 == 0:
        print(subj, pred, obj)

print("graph has {} statements.".format(len(g)))