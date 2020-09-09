from dash_frontend.visualizations.nx_graph_visualization import general_nx_grah_to_cytoscape
from dash_frontend.visualizations.pytables_visualization import main_pytable_visualization
from dash_frontend.state.initialize_demo_state import multi_model_join_results
from dash_frontend.visualizations.tree_visualization import tree_to_cytoscape

def visualize_multi_model_join_result():
    result = multi_model_join_results.get_current_state()
    if result.get_model() == "relational":
        return main_pytable_visualization()
    elif result.get_model() == "graph":
        return general_nx_grah_to_cytoscape()
    elif result.get_model() == "tree":
        return tree_to_cytoscape()