import json
import matplotlib.pyplot as plt
from instance_category.objects.collection_object import CollectionObject
from instance_category.morphisms.morphism import Morphism
from multi_model_join.join import add_to_dict, join, join_relational_xml
from multi_model_join.graph_join.graph_join import join_graph_graph, join_graph_relational
from multi_model_join.relational_join import join_relational_relational_over_functional_morphism
import initialize_demo_datasets.initialize_ecommerce as commerce
from instance_functor.instance_functor import InstanceFunctor
import os
import networkx as nx
dirname = os.path.dirname(__file__)

# citation_data_path = os.path.join(
#     dirname, "..\\data\\Patent\\citation.graph")

# citation_graph = CollectionObject("citation_graph", "property graph", "citation", lambda graph: list(graph.nodes),
# {
#     "vertex": [
#         {"filePath": citation_data_path, "fileformat": "csv", "schema": ["citing","cited"], "keyAttribute": ["citing","cited"], "separator": ","}],
#     "edge": [
#         {"filePath": citation_data_path, "fileformat": "csv", "schema": ["citing","cited"], "keyAttribute": ["citing","cited"], "fromKeyAttribute": "citing", 
#         "toKeyAttribute": "cited", "separator": ","}]
# })

# print(nx.number_of_edges(citation_graph.get_collection()))

# for elem in nx.neighbors(citation_graph.get_collection(), "3897377"):
#     print(elem)