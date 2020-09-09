from initialization_of_demo_databases.initialize_ecommerce import ECommerceMultiModelDatabase
#from initialization_of_demo_databases.initialize_patent_data import PatentMultiModelDatabase
#from supportive_functions.row_manipulations import find_values_from_tree
#from supportive_functions.compositions import tree_to_nx_graph
import networkx as nx
import matplotlib.pyplot as plt
#from supportive_functions.compositions import compose_lambda_functions
from external_database_connections.postgresql.postgres import Postgres
from external_database_connections.neo4j.neo4j import Neo4j
from model_transformations.cat_graph import CatGraph
from dash_frontend.visualizations.pytables_visualization import pytables_visualization
import dash
import dash_table
import pandas as pd
import dash_core_components as dcc
import uuid
from supportive_functions.xml_to_dict import XmlDictConfig, XmlListConfig

# dvdrental_relational_to_rdf_uri = "postgresql+psycopg2://postgres:0000@localhost:5432/catGraph"
# dvdrental_property_graph_to_rdf_uri = "postgresql+psycopg2://postgres:0000@localhost:5432/catGraph2"

# #patent_db = PatentMultiModelDatabase()
ecommerce_db = ECommerceMultiModelDatabase()

# # app = dash.Dash(__name__)

# # print(ecommerce_db.get_multi_model_db().get_objects()["location"].get_collection())

# # app.layout = dcc.Graph(figure= pytables_visualization(ecommerce_db.get_multi_model_db().get_objects()["location"].get_collection(). 50))

# # if __name__ == '__main__':
# #     app.run_server(debug=True)

# db = Postgres("dvdrental")
# graph_db = Neo4j("dvdrental")

# catgraph = CatGraph("test_graph", db, dvdrental_relational_to_rdf_uri)
# catgraph.transform_from()
# g = catgraph.get_cat_graph()

# # i = 0
# # for subj, pred, obj in g:
# #     i+=1
# #     if i % 10000 == 0:
# #         print(subj, pred, obj)

# print("graph has {} statements.".format(len(g)))

# catgraph = CatGraph("test_graph2", graph_db, dvdrental_property_graph_to_rdf_uri)
# catgraph.transform_from()
# g = catgraph.get_cat_graph()

# i = 0
# for subj, pred, obj in g:
#     i+=1
#     if i % 1000 == 0:
#         print(subj, pred, obj)

# print("graph has {} statements.".format(len(g)))

def walk_tree(previous_id, root, tree, nodes, edges):
    if type(root) == dict or type(root) == XmlDictConfig:
        for key in root:
            tag_id = uuid.uuid4()
            nodes.append({'data': {'id': tag_id, 'label': key}})
            edges.append({'source': previous_id, 'target': tag_id})
            walk_tree(tag_id, root[key], tree, nodes, edges)
    elif type(root) == list or type(root) == XmlListConfig:
        for elem in root:
            walk_tree(previous_id, elem, tree, nodes, edges)
    else:
        tag_id = uuid.uuid4()
        nodes.append({'data': {'id': tag_id, 'label': str(root)}})
        edges.append({'source': previous_id, 'target': tag_id})
        try:
            walk_tree(tag_id, tree[root], tree, nodes, edges)
        except:
            pass

#result = multi_model_join_results.get_current_state()
T = ecommerce_db.get_multi_model_db().get_objects()["orders"].get_collection().get_tree()
nodes, edges = [], []
for elem in T:
    walk_tree("root", elem, T, nodes, edges)
print(nodes, edges)