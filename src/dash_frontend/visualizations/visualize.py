import dash_html_components as html
from abstract_category.functor.functor_error import Error
from multicategory.initialize_multicategory import multicategory
from dash_frontend.visualizations.pytables_visualization import main_pytable_visualization
from dash_frontend.visualizations.tree_visualization import tree_to_cytoscape
from dash_frontend.visualizations.nx_graph_visualization import general_nx_grah_to_cytoscape
from external_database_connections.neo4j.create_neo4j_query_tool import create_neo4j_query_tool
from external_database_connections.neo4j.neo4j import Neo4j
from external_database_connections.postgresql.create_postgres_query_tool import create_postgres_query_tool
from external_database_connections.postgresql.postgres import Postgres

def visualize(selected_dataset):
    try:
        if type(selected_dataset) == Postgres:
            return create_postgres_query_tool()
        elif type(selected_dataset) == Neo4j:
            return create_neo4j_query_tool()
        else:
            if selected_dataset.get_model() == "relational":
                return main_pytable_visualization(selected_dataset)
            elif selected_dataset.get_model() == "graph":
                return general_nx_grah_to_cytoscape(selected_dataset)
            elif selected_dataset.get_model() == "tree":
                return tree_to_cytoscape(selected_dataset)
    except Error as e:
        return html.Div("Error in visualization: " + str(e))