from initialization_of_demo_databases.initialize_ecommerce import ECommerceMultiModelDatabase
from initialization_of_demo_databases.initialize_patent_data import PatentMultiModelDatabase
from dash_frontend.tabs.instance_functor_tab import nx_graph_to_plotly, nx_grah_to_cytoscape
from dash_frontend.state.initialize_demo_state import state
import inspect
from supportive_functions.row_manipulations import find_values_from_tree
from supportive_functions.compositions import tree_to_nx_graph
import networkx as nx
import uuid
import matplotlib.pyplot as plt
from supportive_functions.compositions import compose_lambda_functions

patent_db = PatentMultiModelDatabase()
ecommerce_db = ECommerceMultiModelDatabase()

#print(ecommerce_db.get_multi_model_db().get_morphisms_for_pair_of_objects("site", "location"))

# result_model = state.get_current_state()["db"].get_objects()["site"].get_model()

# lambda_function = state.get_current_state()["db"].get_morphisms()["customer_to_location_morphism"].get_collection_relationship().get_lambda_function()
# code_lines = inspect.getsource(lambda_function)
# print(code_lines)
ecommerce_db.run_multi_model_join_examples()

# ## elem["customer_id"] for elem in key_value_pairs.get_iterable_collection_of_objects()["orders_to_customers"] if order["Order_no"] == elem["order_id"]
#orders = ecommerce_db.get_multi_model_db().get_objects()["orders"].get_collection().find_elements_with_attribute("Orders")
#print(orders)
#print(dict(orders))
# for order in orders:
#     #for order2 in orders[order]:
#         #print(order2)
#     value = True in [True for order2 in orders[order] if order2["Order_no"] == '34e5e79']
#     print(value)
# for elem in ecommerce_db.get_multi_model_db().get_objects()["key_value_pairs"].get_collection().get_iterable_collection_of_objects()["orders_to_customers"]:
#     print(elem["customer_id"])

# key_value_pairs = ecommerce_db.get_multi_model_db().get_objects()["key_value_pairs"].get_collection()
# customer_graph = ecommerce_db.get_multi_model_db().get_objects()["customer"].get_collection()

# lambda1 = lambda order : [elem for elem in key_value_pairs.get_iterable_collection_of_objects()["orders_to_customers"] if True in [True for order2 in order["Orders"] if order2["Order_no"] == elem["order_id"]]]
# lambda2 = lambda elem : [customer for customer in customer_graph.get_iterable_collection_of_objects() if len(customer) == 2 and str(elem["customer_id"]) == customer[1]["customer_id"]]

# example_order = {"Orders": [{'Order_no': '34e5e79', 'Product': {'Product_no': '3424g', 'Product_Name': 'Book', 'Price': '40'}}]}

# # def lambda1(order):
# #     result = []
# #     for elem in key_value_pairs.get_iterable_collection_of_objects()["orders_to_customers"]:
# #         for order2 in order["Orders"]:
# #             if order2["Order_no"] == elem["order_id"]:
# #                 print(elem)
# #                 result.append(elem)
# #     return result

# print(lambda1(example_order))

# for elem in lambda1(example_order):
#     print(lambda2(elem))

# comp = compose_lambda_functions(lambda2, lambda1)

# print(comp(orders))
# # for elem in orders:
# #     print(elem)
# #     print(comp(elem))


# patent_db.run_model_category_join_examples()
# patent_db.run_multi_model_join_examples()

# G = ecommerce_db.get_multi_model_db().get_instance_category_nx_graph()
# fig = nx_grah_to_cytoscape(G)
# print(G.number_of_edges(), G.number_of_nodes())
# graph = nx.DiGraph()
# orders = {"root": {"first": ["value1", "value2"], "second": 7}} #ecommerce_db.get_multi_model_db().get_objects()["orders"].get_collection().get_iterable_collection_of_objects()
# tree_to_nx_graph(dict(orders), graph, uuid.uuid4())

# print(graph.nodes.data())

# nx.draw(graph, with_labels=True)
# plt.show()