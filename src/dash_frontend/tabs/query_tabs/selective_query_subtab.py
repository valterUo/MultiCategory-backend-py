import dash
import dash_core_components as dcc
import dash_html_components as html
from dash_frontend.state.initialize_demo_state import state
from dash_frontend.server import app
from dash_frontend.modal.fold_query_modal import generate_fold_query_modal
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash_frontend.fold_query_processing_frontend.execute_query import execute_query
from dash_frontend.fold_query_processing_frontend.render_return_attribute_input import render_return_attribute_input
fold_query_state = []


def selective_query_subtab():
    return dcc.Tab(
        id="Selective-query-tab",
        label="Selective queries",
        value="subtab1",
        className="custom-tab",
        selected_className="custom-tab--selected",
    )


def build_selective_query_subtab():
    objects = state.get_current_state()["db"].get_objects()
    initial_options = []
    for obj in objects:
        initial_options.append({'label': str(obj), 'value': str(obj)})
    examples = state.get_current_state()["filtering_examples"]

    return [html.Div(id="query-tab-main-container", children=[
        html.Div(
            id="set-specs-intro-container",
            children=[
                html.H4(
                    "This area is for creating selective queries and creating new objects and morphisms to the selected multi-model database."
                ),
                html.Hr(),
                html.Div(
                    id="folding-tool",
                    children=[
                        html.Div(id="fold-query-creator-title", style={"width": "100%", "display": "inline-block"},
                                 children=[
                                 html.H6(
                                    "Create a new collection and morphism from the existing collection", style={'display': 'inline-block'}),
                                 html.Button(id="learn-more-fold-function-button",
                                             children="LEARN MORE", style={"marginLeft": "10px"}),
                                 generate_fold_query_modal()
                                 ]),
                        html.Div(id="query-name", style={"border": "1px solid white", "padding": "10px", "margin": "10px"},
                                 children=[
                            html.Label([
                                "Input name for this query", html.Br(),
                                dcc.Input(
                                    id="query-name-input",
                                    type="text",
                                    value="",
                                    placeholder="name",
                                    style={'width': '90%',
                                           "display": "block"},
                                )])
                        ]),
                        html.Div(id="fold-query-creator", style={"width": "50%", "display": "inline-block", 'float': 'left', "borderRight": "1px solid white"}, children=[
                            html.Div(id="fold-function-block", children=[
                                html.Div(style={"border": "1px solid white", "padding": "10px", "margin": "10px"}, children=html.Label([
                                        "Select queried domain dataset",
                                        dcc.Dropdown(
                                            id="select-query-domain-dataset",
                                            style={'width': '90%',
                                                            "display": "block"},
                                            options=initial_options,
                                            disabled=False,
                                        )])),
                                html.Div(id="filtering-condition-and-examples", style={"border": "1px solid white", "padding": "10px", "margin": "10px"},
                                         children=[
                                    html.Label([
                                        "Input filtering condition for this block", html.Br(),
                                        dcc.Input(
                                            id="lambda-function-input",
                                            type="text",
                                            value="",
                                            placeholder="filtering condition",
                                            style={'width': '90%',
                                                   "display": "inline-block"},
                                        )]), html.Br(), html.Label([
                                            "Examples", html.Br(),
                                            dcc.Dropdown(
                                                id="filtering-example-dropdown",
                                                style={'width': '90%',
                                                       "display": "block"},
                                                options=examples,
                                            )])]),
                                html.Div(id="return-attribute-input-container", style={
                                         "border": "1px solid white", "padding": "10px", "margin": "10px"}, children=render_return_attribute_input("relational", fold_query_state)),
                                html.Div(style={"border": "1px solid white", "padding": "10px", "margin": "10px"}, children=html.Label([
                                    "Select target data model",
                                    dcc.Dropdown(
                                        id="select-target-data-model",
                                        style={'width': '90%',
                                                        "display": "block"},
                                        options=[{'label': 'relational', 'value': 'relational'},
                                                 {'label': 'property graph',
                                                           'value': 'graph'},
                                                 {'label': 'tree',
                                                           'value': 'tree'},
                                                 {'label': 'RDF graph',
                                                           'value': 'RDF'},
                                                 {'label': 'String',
                                                           'value': 'String'},
                                                 {'label': 'Int',
                                                  'value': 'Int'},
                                                 {'label': 'Boolean',
                                                  'value': 'Boolean'}],
                                        value='relational',
                                    )])),
                            ]),
                            html.Br(),
                            html.Button(id="append-query-block",
                                        children="APPEND QUERY BLOCK")
                        ]
                        ),
                        html.Div(id="current-query-view", style={"width": "49%", "display": "inline-block", 'float': 'left'}, children=[
                            html.H6("The current query: ",
                                    style={"margin": "5px"}),
                            html.Div(id="current-query", children=[]),
                            html.Button(id="execute-fold-query-button",
                                        children="EXECUTE",
                                        n_clicks=0, style={"marginLeft": "10px"}),
                        ]),
                    ]),
                html.Div(id="result-notification")
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
    [Output("current-query", "children"),
     Output("select-query-domain-dataset", "disabled")],
    [Input("append-query-block", "n_clicks")],
    [State("select-query-domain-dataset", "value"),
     State("lambda-function-input", "value"),
     State("return-attributes-input", "value"),
     State("return-attribute-dropdown", "value"),
     State("return-attribute-vertex-input", "value"),
     State("return-attribute-vertex-dropdown", "value"),
     State("return-attribute-edge-input", "value"),
     State("return-attribute-edge-dropdown", "value"),
     State("select-target-data-model", "value"),
     State("current-query", "children")]
)
def append_to_query(button_click, domain, lambda_input, return_attributes, attributes, return_attributes_vertices, attributes_vertices, return_attributes_edges, attributes_edges, target_model, current_children):
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "append-query-block":
            if domain == None or lambda_input == "" or target_model == None:
                raise PreventUpdate
            if return_attributes != "" or attributes != None:
                return handle_relational_tree_query_blocks(domain, lambda_input, return_attributes, attributes, target_model, current_children)
            else:
                return handle_graph_query_block(domain, lambda_input, return_attributes_vertices, attributes_vertices, return_attributes_edges, attributes_edges, target_model, current_children)
    else:
        raise PreventUpdate


def handle_relational_tree_query_blocks(domain, lambda_input, return_attributes, attributes, target_model, current_children):
    if attributes == None:
        attributes = []
    if return_attributes != "":
        attributes = attributes + return_attributes.split(",")
    block = dict()
    global fold_query_state
    if fold_query_state == []:
        block["domain"] = domain
    else:
        domain = "previous block"
    block["lambda_input"] = lambda_input
    block["return_attributes"] = attributes
    block["target_model"] = target_model
    fold_query_state.append(block)
    current_children.append(
        html.Div(style={"width": "100%"}, children=[
            html.Div(style={"margin": "10px", "border": "1px solid white"}, children=[
                html.Div(style={"margin": "10px"}, children=[
                    html.H6("Query block"),
                    html.P("Query from: " + domain),
                    html.P("With function: " + lambda_input),
                    html.P("With return attirbutes: " +
                           ", ".join(attributes)),
                    html.P("Result will be in model: " + target_model),
                ])]), html.Div(style={"margin": "10px auto", "width": "1%"},  children=[html.Span(className="arrow down")])
        ])
    )
    return current_children, True


def handle_graph_query_block(domain, lambda_input, return_attributes_vertices, attributes_vertices, return_attributes_edges, attributes_edges, target_model, current_children):
    if attributes_vertices == None:
        attributes_vertices = []
    if attributes_edges == None:
        attributes_edges = []
    if return_attributes_vertices != "":
        attributes_vertices = attributes_vertices + \
            return_attributes_vertices.split(",")
    if return_attributes_edges != "":
        attributes_edges = attributes_edges + \
            return_attributes_edges.split(",")
    block = dict()
    global fold_query_state
    if fold_query_state == []:
        block["domain"] = domain
    else:
        domain = "previous block"
    block["lambda_input"] = lambda_input
    block["return_attributes"] = {
        "vertex_object_attributes": attributes_vertices, "edge_object_attributes": attributes_edges}
    block["target_model"] = target_model
    fold_query_state.append(block)
    current_children.append(
        html.Div(style={"width": "100%"}, children=[
            html.Div(style={"margin": "10px", "border": "1px solid white"}, children=[
                html.Div(style={"margin": "10px"}, children=[
                    html.H6("Query block"),
                    html.P("Query from: " + domain),
                    html.P("With function: " + lambda_input),
                    html.P("With return attirbutes on vertices with: " +
                           ", ".join(attributes_vertices)),
                    html.P("With return attirbutes on edges with: " +
                           ", ".join(attributes_edges)),
                    html.P("Result will be in model: " + target_model),
                ])]), html.Div(style={"margin": "10px auto", "width": "1%"}, children=[html.Span(className="arrow down")])
        ])
    )
    return current_children, True


@app.callback(
    Output("result-notification", "children"),
    [Input("execute-fold-query-button", "n_clicks")],
    [State("query-name-input", "value")]
)
def update_click_output(button_click, name):
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "execute-fold-query-button":
            global fold_query_state
            result = execute_query(name, fold_query_state)
            fold_query_state = []
            return html.H6("The final result with name " + result.get_name() + " and all the blocks can be viewed in the result tab.")
    else:
        raise PreventUpdate


@app.callback(
    Output("lambda-function-input", "value"),
    [Input("filtering-example-dropdown", "value")]
)
def select_filtering_example(selected_example):
    if selected_example != None:
        return selected_example
    else:
        raise PreventUpdate


@app.callback(
    Output("return-attribute-dropdown", "options"),
    [Input("select-query-domain-dataset", "value")]
)
def update_return_attributes(selected_domain):
    if selected_domain != None:
        data_object = state.get_current_state()["db"].get_objects()[
            selected_domain]
        domain_model = data_object.get_model()
        if domain_model != None and domain_model != "graph":
            attributes = data_object.get_attributes_from_model_category()
            options = [{'label': str(value), 'value': str(value)}
                       for value in attributes]
            return options
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback(
    [Output("return-attribute-vertex-dropdown", "options"),
     Output("return-attribute-edge-dropdown", "options")],
    [Input("select-query-domain-dataset", "value")]
)
def update_return_attributes_graph(selected_domain):
    if selected_domain != None:
        data_object = state.get_current_state()["db"].get_objects()[
            selected_domain]
        domain_model = data_object.get_model()
        if domain_model == "graph":
            attributes = data_object.get_attributes_from_model_category()
            vertices = [{'label': str(value), 'value': str(value)}
                        for value in attributes["vertices"]]
            edges = [{'label': str(value), 'value': str(value)}
                     for value in attributes["edges"]]
            return vertices, edges
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback(
    Output("return-attribute-input-container", "children"),
    [Input("select-query-domain-dataset", "value")]
)
def update_return_attributes(selected_domain):
    if selected_domain != None:
        data_object = state.get_current_state()["db"].get_objects()[
            selected_domain]
        domain_model = data_object.get_model()
        return render_return_attribute_input(domain_model, fold_query_state)
    else:
        raise PreventUpdate
