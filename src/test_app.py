from initialization_of_demo_databases.initialize_ecommerce import ECommerceMultiModelDatabase
from initialization_of_demo_databases.initialize_patent_data import PatentMultiModelDatabase
from initialization_of_demo_databases.initialize_unibench_sf10 import UnibenchMultiModelDatabase
from category_of_collection_constructor_functors.model_categories.category_of_graph_model import GraphModelCategory
from category_of_collection_constructor_functors.model_categories.category_of_table_model import TableModelCategory
from category_of_collection_constructor_functors.model_categories.overlay_model_categories import overlay_model_categories
from dash_frontend.visualizations.nx_graph_visualization import parse_cytoscape_nodes_edges

import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx

# patent_db = PatentMultiModelDatabase()
# ecommerce_db = ECommerceMultiModelDatabase()
# unibench = UnibenchMultiModelDatabase("SF30")

# graph = GraphModelCategory("test", ["graphID", "name"], ["knows"])
# table = TableModelCategory("table_test", ["tableID", "location"])

# graph_id = graph.get_vertex_object().get_id()
# table_id = table.get_objects()[0].get_id()
# table_id2 = table.get_objects()[1].get_id()

# result = overlay_model_categories(graph, graph_id, table, table_id)
# result = overlay_model_categories(result, result.get_objects()[0].get_id(), table, table_id2)

# print(result.get_nx_graph().number_of_nodes())

# G = result.get_nx_graph()

# print(parse_cytoscape_nodes_edges(G))