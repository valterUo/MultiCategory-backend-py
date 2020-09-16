import dash
import dash_core_components as dcc
import dash_html_components as html
from multi_model_join.multi_model_join import MultiModelJoin
from dash_frontend.multi_model_join_frontend.visualize_multi_model_join_result import visualize_multi_model_join_result
from dash_frontend.state.initialize_demo_state import multi_model_join_results


def execute_multi_model_join(state, join_parameters):
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
    database.add_morphism(join_result.get_left_leg())
    database.add_morphism(join_result.get_right_leg())

    multi_model_join_results.update_possible_states(result.get_name(), result)
    multi_model_join_results.change_state(result.get_name())
    
    return visualize_multi_model_join_result()