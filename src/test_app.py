from initialization_of_demo_databases.initialize_ecommerce import ECommerceMultiModelDatabase
from initialization_of_demo_databases.initialize_patent_data import PatentMultiModelDatabase
from dash_frontend.tabs.instance_functor_tab import nx_graph_to_plotly, nx_grah_to_cytoscape

patent_db = PatentMultiModelDatabase()
print(patent_db.get_multi_model_db())
ecommerce_db = ECommerceMultiModelDatabase()
print(ecommerce_db.get_multi_model_db())

#ecommerce_db.run_multi_model_join_examples()

#patent_db.run_model_category_join_examples()
#patent_db.run_multi_model_join_examples()

G = ecommerce_db.get_multi_model_db().get_instance_category_nx_graph()
fig = nx_grah_to_cytoscape(G)
print(G.number_of_edges(), G.number_of_nodes())