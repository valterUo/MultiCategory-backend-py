import dash
import dash_core_components as dcc
import dash_html_components as html
from dash_frontend.state.initialize_demo_state import state
from dash_frontend.server import app
from dash_frontend.modal.fold_query_modal import generate_fold_query_modal
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

def query_tab():
    return dcc.Tab(
        id="Query-tab",
        label="Queries",
        value="tab3",
        className="custom-tab",
        selected_className="custom-tab--selected",
    )


def build_query_tab():
    objects = state.get_current_state()["db"].get_objects()
    initial_options = []
    for obj in objects:
        print(obj)
        initial_options.append({'label': str(obj), 'value': str(obj)})

    return [html.Div(id="query-tab-main-container", children=[
        html.Div(
            id="set-specs-intro-container",
            children=[
                html.H4(
                    "This area is for creating selective queries and creating new objects and morphisms to the selected multi-model database."
                ),
                html.Hr(),
                html.Label(children=[
                    html.H6("Visualize the whole selected dataset: "),
                    dcc.Dropdown(
                        id="select-all-query-dropdown",
                        style={'width': '50%'},
                        options=initial_options,
                    )]),
                html.Hr(),
                html.Div(
                    id="folding-tool",
                    children=[
                        html.Div(id="fold-query-creator-title", style={"width": "100%", "display": "inline-block"},
                                     children=[
                                 html.H6(
                                    "Create a new collection and morphism from the existing collection.", style={'display': 'inline-block'}),
                                 html.Button(id="learn-more-fold-function-button",
                                             children="LEARN MORE",
                                             n_clicks=0, style={"marginLeft": "10px", "height": "30px"}),
                                 generate_fold_query_modal()
                                 ]),
                        html.Div(id="fold-query-creator", style={"width": "50%", "display": "inline-block", 'float':'left', "borderRight": "1px solid white"}, children=[
                            html.Div(id="fold-function-block", children=[
                                html.Label([
                                        "Select queried domain dataset",
                                        dcc.Dropdown(
                                            id="select-query-domain-dataset",
                                            style={'width': '49%',
                                                   "display": "block"},
                                            options=initial_options,
                                        )]),
                                html.Br(),
                                html.Label([
                                    "Input filtering condition used in the lambda function",
                                    dcc.Input(
                                        id="lambda-function-input",
                                        type="text",
                                        placeholder="lambda function input",
                                        style={'width': '49%',
                                               "display": "block"},
                                    )]),
                                html.Br(),
                                html.Label([
                                    "Select target data model",
                                    dcc.Dropdown(
                                        id="select-target-data-model",
                                        style={'width': '49%',
                                               "display": "block"},
                                        options=[{'label': 'relational', 'value': 'relational'},
                                                 {'label': 'property graph',
                                                  'value': 'graph'},
                                                 {'label': 'tree: JSON',
                                                  'value': 'JSON'},
                                                 {'label': 'tree: XML',
                                                  'value': 'XML'},
                                                 {'label': 'RDF graph', 'value': 'RDF'}],
                                        value='relational',
                                    )]),
                            ]), 
                            html.Br(),
                            html.Button(id="append-query-block", children="APPEND QUERY BLOCK")
                        ]
                        ),
                        html.Div(id="current-query-view", style={"width": "49%", "display": "inline-block", 'float':'left'}, children=[
                                html.P("The current query: ", style = {"margin": "5px"}),
                                html.Div(id="current-query")
                            ]),
                    ]),
                # html.Hr(),
                # html.Div(
                #     id="create-new-morphism-functor-tool",
                #     children=[
                #         html.H6(
                #             "Create a new morphism between existing collections.")
                #     ]
                # ),
                # html.Hr(),
                # html.Div(
                #     id="create-new-collection-constructor-functor-tool",
                #     children=[
                #         html.H6(
                #             "Create a new (empty) collection constructor functor.")
                #     ]
                # ),
            ])]
    )]


@app.callback(
    Output("markdown-fold-query", "style"),
    [Input("learn-more-fold-function-button", "n_clicks"),
     Input("markdown_close_fold", "n_clicks")],
)
def update_click_output(button_click, close_click):
    ctx = dash.callback_context

    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "learn-more-fold-function-button":
            return {"display": "block"}
    return {"display": "none"}

@app.callback(
    Output("current-query", "children"),
    [Input("append-query-block", "n_clicks")],
    [State("select-query-domain-dataset", "options"), 
    State("lambda-function-input", "value"), 
    State("select-target-data-model", "options")]
)
def append_to_query(button_click, domain, lambda_input, target_model):
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "append-query-block":
            return {"display": "block"}
    else:
        raise PreventUpdate
