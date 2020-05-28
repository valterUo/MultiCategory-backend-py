from functools import reduce
import networkx as nx
import json
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from instance_category.objects.collection_object import CollectionObject
from instance_category.morphisms.morphism import Morphism
from multi_model_join.join import add_to_dict, join, join_relational_xml
from multi_model_join.graph_join.graph_join import join_graph_graph, join_graph_relational
import initialize_demo_datasets.initialize_ecommerce as commerce

commerce.init()
objects = commerce.e_commerce_instance.get_objects()
morphisms = commerce.e_commerce_instance.get_morphisms()

join_graph = join_graph_relational(objects["customersGraph"], morphisms["located"], objects["locationsTable"])

print(join_graph)

print(join_graph)
plt.subplot(111)
nx.draw(join_graph.getCollection(), with_labels=False, font_weight='bold')
plt.show()