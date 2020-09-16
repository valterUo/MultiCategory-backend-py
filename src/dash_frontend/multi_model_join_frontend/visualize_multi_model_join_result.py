from dash_frontend.visualizations.multi_model_join_nx_graph_visualization import general_nx_grah_to_cytoscape
from dash_frontend.visualizations.model_category_join_nx_graph_visualization import model_category_nx_grah_to_cytoscape
from dash_frontend.visualizations.pytables_visualization import main_pytable_visualization
from dash_frontend.state.initialize_demo_state import multi_model_join_results
from dash_frontend.visualizations.tree_visualization import tree_to_cytoscape

def visualize_multi_model_join_result():
    join_result = multi_model_join_results.get_current_state()
    result = join_result.get_result()
    if result.get_model() == "relational":
        return main_pytable_visualization()
    elif result.get_model() == "graph":
        return general_nx_grah_to_cytoscape()
    elif result.get_model() == "tree":
        return tree_to_cytoscape()

def visualize_join_triangle_with_model_categories():
    return model_category_nx_grah_to_cytoscape()
