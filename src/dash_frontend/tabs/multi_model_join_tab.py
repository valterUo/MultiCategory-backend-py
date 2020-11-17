import dash
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
from dash_frontend.server import app
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import inspect
from dash_frontend.multi_model_join_frontend.multi_model_join import execute_multi_model_join
from dash_frontend.multi_model_join_frontend.second_description_input_builder import second_description_input_builder
from dash_frontend.multi_model_join_frontend.tree_attributes_input_builder import tree_attributes_input_builder
from dash_frontend.server import app
from multicategory.initialize_multicategory import multicategory
from dash_frontend.state.parameter_state import parameter_state


def multi_model_join_tab():
    return dcc.Tab(
        id="Join-tab",
        label="Multi-model join",
        value="tab4",
        className="custom-tab",
        selected_className="custom-tab--selected",
    )


def build_multi_model_join_tab():
    objects = multicategory.get_selected_multi_model_database().get_str_list_of_objects()
    return [html.Div(
            id="set-specs-intro-container",
            children=[
                html.Div(id="multi-model-join-parent-container", style={"margin": "20px"}, children=[
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
                            html.Button(id='submit-domain-target',
                                        children='Search morphisms'),
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
                                html.Div(id="right-left-full-toggle-switches", children=[
                                    html.P("""You can choose left, right or full join. 
                        Left join is defined for all the data model combinations and the right join is defined between graphs. 
                        If the join is not avaible for the combination, the selection (ON/OFF) does not affect to the result. 
                        The idea behind left and right joins is not exactly the same as in the relational data model."""),
                                    daq.BooleanSwitch(
                                        id='left-boolean-switch',
                                        on=False,
                                        persisted_props=['on']
                                    ),
                                    html.Div(id='left-boolean-switch-output'),
                                    daq.BooleanSwitch(
                                        id='right-boolean-switch',
                                        on=False,
                                        persisted_props=['on']
                                    ),
                                    html.Div(id='right-boolean-switch-output')
                                ]),
                                html.Br(),
                                html.Div(id="second_description_input"),
                                html.Br(),
                                html.Div(id="tree_attributes_input"),
                                html.H5(
                                    "The following multi-model join will be executed: "),
                                html.Div(id="overall-join"),
                                html.Br(),
                                html.Button(id='execute-button',
                                            children='Perform multi-model join'),
                            ]
                            ),
                        ]
                    ),
                    html.Div(id="multi-model-result-container")
                ])
            ])]


@app.callback(
    [Output("multi-model-join-morphisms", "options"),
     Output("hiding-element", "style")],
    [Input("submit-domain-target", "n_clicks")],
    [State('multi-model-join-domain', 'value'),
     State('multi-model-join-target', 'value')]
)
def render_object_selection(n_clicks, domain, target):
    global parameter_state
    parameter_state["domain"] = domain
    parameter_state["target"] = target
    ctx = dash.callback_context
    prop_id = ""
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "submit-domain-target":
            if domain != None and target != None:
                database = multicategory.get_selected_multi_model_database()
                result = database.get_morphisms_for_pair_of_objects(
                    domain, target)
                return [o for o in result], {"display": "block"}
            else:
                raise PreventUpdate
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
    global parameter_state
    if value != None:
        db = multicategory.get_selected_multi_model_database()
        parameter_state["morphism"] = value
        result_model = db.get_objects()[parameter_state["domain"]].get_model()
        parameter_state["result_model"] = result_model
        lambda_function = db.get_morphisms(
        )[value].get_collection_relationship().get_lambda_function()
        code_lines = inspect.getsource(lambda_function)
        return [html.P(parameter_state["domain"] + " -- " + value + " --> " + parameter_state["target"]),
                html.P("The result will be in " + result_model + " model."),
                html.P("The morphism is defined with the following lambda function: "),
                html.P(str(code_lines))], {'display': 'block'}
    return [], {'display': 'none'}


@app.callback(
    dash.dependencies.Output('left-boolean-switch-output', 'children'),
    [dash.dependencies.Input('left-boolean-switch', 'on')])
def update_output(on):
    global parameter_state
    parameter_state["left"] = on
    if on:
        return 'The left join is ON'
    else:
        return 'The left join is OFF'


@app.callback(
    dash.dependencies.Output('right-boolean-switch-output', 'children'),
    [dash.dependencies.Input('right-boolean-switch', 'on')])
def update_output(on):
    global parameter_state
    parameter_state["right"] = on
    if on:
        return 'The right join is ON'
    else:
        return 'The right join is OFF'


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
        result_element = execute_multi_model_join(parameter_state)
        return html.Div(result_element), {"display": "none"}
        #return html.Div(dash_dangerously_set_inner_html.DangerouslySetInnerHTML('''<div id = "multi-model-join-loader" class="loader"></div>''')), {"display": "none"}
    else:
        raise PreventUpdate


@app.callback(
    Output("second_description_input", "children"),
    [Input("multi-model-join-morphisms", "value")]
)
def second_description_input_toggle(value):
    objects = multicategory.get_selected_multi_model_database()
    if parameter_state["domain"] != None and parameter_state["target"] != None:
        domain = objects[parameter_state["domain"]].get_model()
        target = objects[parameter_state["target"]].get_model()
        if domain == "relational" and (target == "graph" or target == "tree"):
            return second_description_input_builder(parameter_state)
    return []


@app.callback(
    Output("tree_attributes_input", "children"),
    [Input("multi-model-join-morphisms", "value")]
)
def tree_attributes_input_toggle(value):
    if parameter_state["domain"] != None and parameter_state["target"] != None:
        domain = multicategory.get_selected_multi_model_database().get_objects()[
            parameter_state["domain"]].get_model()
        if domain == "tree":
            return tree_attributes_input_builder(parameter_state)
    return []
