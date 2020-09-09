import dash
import dash_core_components as dcc
import dash_html_components as html
from multi_model_join.multi_model_join import MultiModelJoin
from dash_frontend.multi_model_join_frontend.visualize_multi_model_join_result import visualize_multi_model_join_result
from dash_frontend.state.initialize_demo_state import multi_model_join_results


def execute_multi_model_join(state, join_parameters):
    #print(state, join_parameters)
    domain = state.get_current_state()["db"].get_objects()[join_parameters["domain"]]
    #print(domain.get_name())
    target = state.get_current_state()["db"].get_objects()[join_parameters["target"]]
    #print(target.get_name())
    morphism = state.get_current_state()["db"].get_morphisms()[join_parameters["morphism"]]
    #print(morphism.get_name())
    left = join_parameters["left"]
    right = join_parameters["right"]
    second_description = join_parameters["second_description"]
    tree_attributes = join_parameters["tree_attributes"]
    join_result = MultiModelJoin(domain, morphism, target, left=left, right=right, second_description=second_description, tree_attributes=tree_attributes)
    result = join_result.get_result()
    multi_model_join_results.update_possible_states(result.get_name(), result)
    multi_model_join_results.change_state(result.get_name())
    return visualize_multi_model_join_result()