import dash
import dash_core_components as dcc
import dash_html_components as html
from multi_model_join.multi_model_join import MultiModelJoin
from dash_frontend.tabs.instance_functor_tab import general_nx_grah_to_cytoscape

def execute_multi_model_join(state, join_parameters):
    print(state, join_parameters)
    domain = state.get_current_state()["db"].get_objects()[join_parameters["domain"]]
    print(domain.get_name())
    target = state.get_current_state()["db"].get_objects()[join_parameters["target"]]
    print(target.get_name())
    morphism = state.get_current_state()["db"].get_morphisms()[join_parameters["morphism"]]
    print(morphism.get_name())
    join_result = MultiModelJoin(domain, morphism, target, True)
    result = join_result.get_result()
    print(result.get_model())
    if result.get_model() == "relational":
        return html.Div()
    elif result.get_model() == "graph":
        print(type(result.get_collection().get_graph()))
        return general_nx_grah_to_cytoscape(result.get_collection().get_graph())
    elif result.get_model() == "tree":
        return html.Div()
