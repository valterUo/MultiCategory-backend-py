import dash
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
from dash_frontend.server import app
from dash.dependencies import Input, Output, State
from dash_frontend.state.initialize_demo_state import state, parameter_state
from dash.exceptions import PreventUpdate
import inspect
import dash_dangerously_set_inner_html
from dash_frontend.multi_model_join_frontend.multi_model_join import execute_multi_model_join
from dash_frontend.multi_model_join_frontend.second_description_input_builder import second_description_input_builder
from dash_frontend.multi_model_join_frontend.tree_attributes_input_builder import tree_attributes_input_builder
from dash_frontend.server import app


def result_tab():
    return dcc.Tab(
        id="Result-tab",
        label="Result",
        value="tab6",
        className="custom-tab",
        selected_className="custom-tab--selected",
    )


def build_result_tab():
    objects = state.get_current_state()["db"].get_objects()
    initial_options = []
    for obj in objects:
        print(obj)
        initial_options.append({'label': str(obj), 'value': str(obj)})

    return [html.Div(id="result-tab-main-container", children=[
        html.Div(id = "select-visualized-object", children = [
            html.H4(
                    "This area is for creating selective queries and creating new objects and morphisms to the selected multi-model database."
                ), html.Hr(),
            html.Label(children=[
                    html.H6("Visualize the selected object (includes results to queries): "),
                    dcc.Dropdown(
                        id="select-all-query-dropdown",
                        style={'width': '50%'},
                        options=initial_options,
                    )]),
                html.Hr(),
        ])
    ])]