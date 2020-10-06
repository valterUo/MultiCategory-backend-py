import dash
import dash_cytoscape as cyto
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash_frontend.server import app
from dash.exceptions import PreventUpdate
import json
from dash_frontend.state.initialize_demo_state import state
from constructing_multi_model_db.collection_constructor.construct_converged_collection_constructor_functor import construct_converged_collection_constructor_functor
nodes, edges, model_categories, added_connections = [], [], [], []
domain, target = None, None

"""
Cytoscape nodes {'data': {'id': 'one', 'label': 'Node 1'}, 'position': {'x': 50, 'y': 50}}
Cytoscape edges {'data': {'source': 'one', 'target': 'two', 'label': 'Node 1 to 2'}}
"""

def parse_cytoscape_nodes_edges(G):
    nodes, edges = [], []
    for node in G.nodes.data():
        print(node[1]["label"])
        nodes.append(
            {'data': {'id': str(node[0]), 'label': node[1]["label"]}})
    for edge in G.edges.data():
        edges.append(
            {'data': {'source': str(edge[0]), 'target': str(edge[1]), 'label': edge[2]["label"]}})
    return nodes, edges


def model_category_building_tool(new_model_category):
    global nodes, edges, model_categories
    model_categories.append(new_model_category)
    added_graph = new_model_category.get_nx_graph()
    added_nodes, added_edges = parse_cytoscape_nodes_edges(added_graph)
    nodes, edges = nodes + added_nodes, edges + added_edges
    #print(nodes, edges)
    cyto_fig = html.Div(children=[ 
        html.Label([
            "Give a name for this converged data model", html.Br(),
            dcc.Input(
                id="object-name-input",
                type="text",
                value="",
                placeholder="name",
                style={'width': '90%',
                        "display": "inline-block"},
            )]), 
            html.Br(),
        cyto.Cytoscape(
            id='cytoscape-result',
            layout={'name': 'circle'},
            style={'width': '90%', 'margin': '0 auto',
                   'height': '800px', 'backgroundColor': '#f8f7ed'},
            elements=nodes + edges,
            stylesheet=[
                {
                    'selector': 'node',
                    'style': {
                        'content': 'data(label)',
                        'color': 'black'
                    }
                },
                {
                    'selector': 'edge',
                    'style': {
                        'content': 'data(label)',
                        'color': 'black',
                        'curve-style': 'bezier',
                        'target-arrow-shape': 'triangle'
                    }
                }
            ]
        ), html.Div(style={"border": "1px solid white", "padding": "10px", "margin": "10px"}, children=[
            html.Pre(id='cytoscape-tapNodeData-domain', style={
                'border': 'thin lightgrey solid', 'margin': '0 auto',
                'overflowX': 'scroll', 'width': '90%'}, children="Select domain node")]),
        html.Div(style={"border": "1px solid white", "padding": "10px", "margin": "10px"}, children=[
            html.Pre(id='cytoscape-tapNodeData-target', style={
                'border': 'thin lightgrey solid', 'margin': '0 auto',
                'overflowX': 'scroll', 'width': '90%'}, children="Select target node")]),
        html.Button(id="combine-domain-target", children="COMBINE SELECTED DOMAIN AND TARGET"),
        html.Br(),
        html.Button(id = "submit-final-model-category", children = "SUBMIT FINAL MODEL CATEGORY"),
        html.Div(id = "create-object-notification")])
    return cyto_fig


@app.callback(Output('cytoscape-tapNodeData-domain', 'children'),
              [Input('cytoscape-result', 'selectedNodeData')])
def displayTapNodeData(node_list):
    global domain
    if node_list != None:
        if len(node_list) == 1:
            data = node_list[0]
            for node in nodes:
                if node["data"]["id"] == data["id"]:
                    domain = node
                    return json.dumps(node["data"], indent=2)
        elif len(node_list) == 0:
            return "Select domain node"
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback(Output('cytoscape-tapNodeData-target', 'children'),
              [Input('cytoscape-result', 'selectedNodeData')])
def displayTapEdgeData(node_list):
    global target
    if node_list != None:
        if len(node_list) == 2:
            data = node_list[1]
            for node in nodes:
                if node["data"]["id"] == data["id"] and data["id"] != domain["data"]["id"]:
                    target = node
                    return json.dumps(node["data"], indent= 2)
        elif len(node_list) == 1:
            return "Select target node"
        else:
            raise PreventUpdate
    else:
            raise PreventUpdate

@app.callback(
    Output("cytoscape-result", "elements"),
    [Input("combine-domain-target", "n_clicks")]
)
def update_click_output(n_clicks):
    global edges, domain, target, added_connections
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "combine-domain-target" and domain != None and target != None:
            added_connections.append((domain["data"]["id"], target["data"]["id"]))
            edges.append({'data': {'source': domain["data"]["id"], 'target': target["data"]["id"], 'label': "new edge"}})
            domain, target = None, None
            return nodes + edges
    raise PreventUpdate

@app.callback(
    Output("create-object-notification", "children"),
    [Input("submit-final-model-category", "n_clicks")],
    [State("object-name-input", "value")]
)
def update_click_output(n_clicks, name):
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "submit-final-model-category" and len(model_categories) > 0 and name != "":
            new_object = construct_converged_collection_constructor_functor(name, model_categories, added_connections)
            state.get_current_state()["db"].add_object(new_object)
            return [html.P("New collection constructor created with the given model category. The constructor is part of the multi-model database. You can insert data into the collection in the insert tab.")]
    else:
        raise PreventUpdate
