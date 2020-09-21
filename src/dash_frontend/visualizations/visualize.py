from dash_frontend.state.initialize_demo_state import state
from dash_frontend.visualizations.pytables_visualization import main_pytable_visualization
from dash_frontend.visualizations.tree_visualization import tree_to_cytoscape
from dash_frontend.visualizations.nx_graph_visualization import general_nx_grah_to_cytoscape

def visualize(selected_dataset):
    objects = state.get_current_state()["db"].get_objects()
    visualized_object = objects[selected_dataset]
    print(visualized_object)
    if visualized_object.get_model() == "relational":
        return main_pytable_visualization(visualized_object)
    elif visualized_object.get_model() == "graph":
        return general_nx_grah_to_cytoscape(visualized_object)
    elif visualized_object.get_model() == "tree":
        return tree_to_cytoscape(visualized_object)