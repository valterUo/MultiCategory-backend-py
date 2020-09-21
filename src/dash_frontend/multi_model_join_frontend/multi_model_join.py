import dash_html_components as html
from multi_model_join.multi_model_join import MultiModelJoin
from dash_frontend.visualizations.visualize import visualize
from dash_frontend.state.initialize_demo_state import state, multi_model_join_results
from dash_frontend.visualizations.model_category_join_nx_graph_visualization import model_category_nx_grah_to_cytoscape


def execute_multi_model_join(join_parameters):
    database = state.get_current_state()["db"]
    domain = database.get_objects()[join_parameters["domain"]]
    target = database.get_objects()[join_parameters["target"]]
    morphism = database.get_morphisms()[join_parameters["morphism"]]
    left = join_parameters["left"]
    right = join_parameters["right"]
    second_description = join_parameters["second_description"]
    tree_attributes = join_parameters["tree_attributes"]
    join_result = MultiModelJoin(domain, morphism, target, left=left, right=right, second_description=second_description, tree_attributes=tree_attributes)
    result = join_result.get_result()
    database.add_object(result)
    #database.add_morphism(join_result.get_left_leg())
    #database.add_morphism(join_result.get_right_leg())
    multi_model_join_results.update_possible_states(join_result.get_name(), join_result)
    multi_model_join_results.change_state(join_result.get_name())
    return html.Div( children = [visualize(result.get_name()), html.Br(), model_category_nx_grah_to_cytoscape()] )