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
from instance_functor.instance_functor import InstanceFunctor

commerce.init()
# objects = commerce.e_commerce_instance.get_objects()
# morphisms = commerce.e_commerce_instance.get_morphisms()

# join_graph = join_graph_relational(objects["customersGraph"], morphisms["located"], objects["locationsTable"])

# print(join_graph)

# print(join_graph)
# plt.subplot(111)
# nx.draw(join_graph.getCollection(), with_labels=False, font_weight='bold')
# plt.show()

# customer1 = frozenset(
#     {('id', '14'), ('locationId', '15'), ('creditLimit', '2900'), ('name', 'Lucas')})
# customer2 = frozenset(
#     {('locationId', '11'), ('name', 'David'), ('id', '23'), ('creditLimit', '1245')})
# customer3 = frozenset(
#     {('id', '7'), ('creditLimit', '9999'), ('locationId', '10'), ('name', 'Bob')})
# customer4 = frozenset(
#     {('name', 'Hannah'), ('creditLimit', '7458'), ('id', '16'), ('locationId', '16')})

# interest1 = frozenset(
#     {('locationId', '13'), ('topic', 'pottery'), ('id', 'I3')})
# interest2 = frozenset(
#     {('locationId', '15'), ('topic', 'volunteering'), ('id', 'I5')})
# interest3 = frozenset(
#     {('locationId', '16'), ('id', 'I6'), ('topic', 'dancing')})


# gluing_graph = nx.DiGraph()
# gluing_graph.add_node(0)

# customerGraph1 = nx.DiGraph()
# customerGraph1.add_nodes_from([customer1])

# customerGraph2 = nx.DiGraph()
# customerGraph2.add_nodes_from([customer4])

# instanceObject1 = CollectionObject(
#     "customers1", "property graph", "customer", lambda graph: list(graph.nodes), None, customerGraph1)
# instanceObject2 = CollectionObject(
#     "customers2", "property graph", "customer", lambda graph: list(graph.nodes), None, customerGraph2)

# def morphism_induced_by_function(customer1, customer2): return True if dict(
#     customer1).get("creditLimit") < dict(customer2).get("creditLimit") else False

# join_graph = join_graph_graph(
#     instanceObject1, morphism_induced_by_function, instanceObject2, gluing_graph)

functor = InstanceFunctor(commerce.e_commerce_instance)
print(functor.get_schema_category())