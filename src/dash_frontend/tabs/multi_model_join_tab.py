import dash
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
from dash_frontend.server import app
from dash.dependencies import Input, Output, State
from dash_frontend.state.initialize_demo_state import state
from dash.exceptions import PreventUpdate
import inspect
import dash_dangerously_set_inner_html
from dash_frontend.multi_model_join_frontend.multi_model_join import execute_multi_model_join
state_dict = {}


def multi_model_join_tab():
    return dcc.Tab(
        id="Join-tab",
        label="Multi-model join",
        value="tab4",
        className="custom-tab",
        selected_className="custom-tab--selected",
    )


def build_multi_model_join_tab(state):
    current_state = state.get_current_state()
    objects = current_state["db"].get_str_list_of_objects()
    print(objects)
    return [html.Div(id="multi-model-join-parent-container", children=[
        html.Div(
            id="multi-model-join-parameters-container",
            children=[
                html.Div(
                    id="set-domain-intro-container",
                    children=[html.P(
                        "Select the domain dataset for multi-model join."
                    ),
                        dcc.Dropdown(
                        id="multi-model-join-domain",
                        style={'width': '50%'},
                        options=objects,
                    ),
                    ]
                ),
                html.Br(),
                html.Div(
                    id="set-target-intro-container",
                    children=[html.P(
                        "Select the target dataset for multi-model join. Note that joins are done over morphisms. "
                    ),
                        dcc.Dropdown(
                        id="multi-model-join-target",
                        style={'width': '50%'},
                        options=objects,
                    ),
                    ]
                ),
                html.Br(),
                html.Button(id='submit-domain-target', type="primary",
                            n_clicks=0, children='Search morphisms'),
                html.Div(id="hiding-element", style={"display": "none"}, children=[
                    html.Br(),
                    html.Div(
                        id="join-morphism-container",
                        children=[html.P(
                            "If there does not exist a suitable morphism from the domain to the target, then you can create new one in the query tab."
                        ),
                            dcc.Dropdown(
                            id="multi-model-join-morphisms",
                            style={'width': '50%'}
                        ),
                        ]
                    ),
                ]), html.Div(id="overall-join-hiding", style={'display': 'none'},
                             children=[
                    html.Br(), 
                    html.Div(id = "right-left-full-toggle-switches", children = [
                        daq.ToggleSwitch(
                            id='left-toggle-switch',
                            value=False
                        ),
                        daq.ToggleSwitch(
                            id='right-toggle-switch',
                            value=False
                        ),
                    ]),
                    html.Div(id='toggle-switch-output'),
                    html.P("The following multi-model join will be executed: "),
                    html.Div(id="overall-join"),
                    html.Br(),
                    html.Button(id='execute-button', n_clicks=0,
                                children='Perform multi-model join'),
                    html.Br(),
                ]
                ),
            ]
        ),
        html.Div(id="multi-model-result-container")
    ])
    ]


@app.callback(
    [Output("multi-model-join-morphisms", "options"),
     Output("hiding-element", "style")],
    [Input("submit-domain-target", "n_clicks")],
    [State('multi-model-join-domain', 'value'),
     State('multi-model-join-target', 'value')]
)
def render_object_selection(n_clicks, domain, target):
    global state_dict
    state_dict = {'domain': domain, 'target': target}
    ctx = dash.callback_context
    prop_id = ""
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if prop_id == "submit-domain-target":
        if domain != None and target != None:
            current_state = state.get_current_state()
            database = current_state["db"]
            result = database.get_morphisms_for_pair_of_objects(domain, target)
            print(type(result))
            return [o for o in result], {"display": "block"}
        else:
           raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback(
    [Output("overall-join", "children"),
     Output("overall-join-hiding", "style")],
    [Input("multi-model-join-morphisms", "value")]
)
def execute_multi_model_join_first_phase(value):
    if value != None:
        global state_dict
        state_dict["morphism"] = value
        result_model = state.get_current_state()["db"].get_objects()[
            state_dict["domain"]].get_model()
        state_dict["result_model"] = result_model
        lambda_function = state.get_current_state()["db"].get_morphisms(
        )[value].get_collection_relationship().get_lambda_function()
        code_lines = inspect.getsource(lambda_function)
        print(code_lines)
        return [html.P(state_dict["domain"] + " -- " + value + " --> " + state_dict["target"]),
                html.P("The result will be in " + result_model + " model."),
                html.P("The morphism is defined with the following lambda function: "),
                html.P(str(code_lines))], {'display': 'block'}


@app.callback(
    [Output("multi-model-result-container", "children"),
     Output("multi-model-join-parameters-container", "style")],
    [Input("execute-button", "n_clicks")]
)
def execute_multi_model_join_second_phase(n_clicks):
    ctx = dash.callback_context
    prop_id = ""
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if prop_id == "execute-button":
        result_element = execute_multi_model_join(state, state_dict)
        print(result_element)
        return html.Div(result_element), {"display": "none"}
        #return html.Div(dash_dangerously_set_inner_html.DangerouslySetInnerHTML('''<div id = "multi-model-join-loader" class="loader"></div>''')), {"display": "none"}
    else:
        raise PreventUpdate

# @app.callback(
#     [Output("multi-model-result-container", "children"), Output("multi-model-join-loader", "style")],
#     [Input("execute-button", "n_clicks")]
# )
# def execute_multi_model_join_third_phase(n_clicks):
#     ctx = dash.callback_context
#     prop_id = ""
#     if ctx.triggered:
#         prop_id = ctx.triggered[0]["prop_id"].split(".")[0]

#     if prop_id == "execute-button":
#         result_element = execute_multi_model_join(state, state_dict)
#         return html.Div(result_element), {"display": "none"}
#     else:
#         raise PreventUpdate
