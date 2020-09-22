import dash_core_components as dcc
import dash_html_components as html
from dash_frontend.state.initialize_demo_state import state
from dash_frontend.visualizations.nx_graph_visualization import nx_grah_to_cytoscape


def define_instance_functor_tab():
    return dcc.Tab(
        id="Instance-tab",
        label="Instance Functor",
        value="tab2",
        className="custom-tab",
        selected_className="custom-tab--selected",
    )


def build_instance_functor_tab():
    database = state.get_current_state()["db"]
    G = database.get_instance_category_nx_graph()
    F = database.get_schema_category_nx_graph()
    instance_fig = nx_grah_to_cytoscape(G)
    schema_fig = nx_grah_to_cytoscape(F)
    return [
        html.Div(id="instance-functor-parent",
                 children=[
                     html.Div(
                         id="set-specs-intro-container",
                         children=[html.H5(
                             "The visualization of the schema and instance categories."), ]
                     ),
                     html.Div(
                         id="schema-category",
                         children=[html.H6("Schema category"), schema_fig]
                     ),
                     html.Div(
                         id="instance-category",
                         children=[
                             html.H6("Instance category"), instance_fig]
                     )
                 ]
                 )
    ]
