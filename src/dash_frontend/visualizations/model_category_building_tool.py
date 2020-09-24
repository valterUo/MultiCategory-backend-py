import dash
import dash_cytoscape as cyto
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash_frontend.server import app
from supportive_functions.json_manipulations import decode_to_json
from dash.exceptions import PreventUpdate
import json
nodes, edges = [], []
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
    global nodes, edges
    added_graph = new_model_category.get_nx_graph()
    added_nodes, added_edges = parse_cytoscape_nodes_edges(added_graph)
    nodes, edges = nodes + added_nodes, edges + added_edges
    print(nodes, edges)
    cyto_fig = html.Div(children=[
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
                'overflowX': 'scroll', 'width': '90%'}, children="Select domain node"), html.Br(),
            html.Button(id="remove-domain-node", children="REMOVE DOMAIN NODE SELECTION")]),
        html.Div(style={"border": "1px solid white", "padding": "10px", "margin": "10px"}, children=[
            html.Pre(id='cytoscape-tapNodeData-target', style={
                'border': 'thin lightgrey solid', 'margin': '0 auto',
                'overflowX': 'scroll', 'width': '90%'}, children="Select target node"), html.Br(),
            html.Button(id="remove-target-node", children="REMOVE TARGET NODE SELECTION")]),
        html.Button(id="combine-domain-target", children="COMBINE SELECTED DOMAIN AND TARGET")])
    return cyto_fig


@app.callback(Output('cytoscape-tapNodeData-domain', 'children'),
              [Input('cytoscape-result', 'tapNodeData'),
               Input("remove-domain-node", "n_clicks")])
def displayTapNodeData(data, n_clicks):
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "remove-domain-node":
            return "Select domain node"
        elif prop_id == "cytoscape-result":
            if data != None:
                for node in nodes:
                    if node["data"]["id"] == data["id"]:
                        global domain
                        domain = node
                        print(node, node["data"]["label"])
                        return json.dumps(node["data"], indent=2)
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback(Output('cytoscape-tapNodeData-target', 'children'),
              [Input('cytoscape-result', 'tapNodeData'),
               Input("remove-target-node", "n_clicks")])
def displayTapEdgeData(data, n_clicks):
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "remove-target-node":
            return "Select target node"
        elif prop_id == "cytoscape-result" and domain != None:
            if data != None:
                for node in nodes:
                    if node["data"]["id"] == data["id"]:
                        global target
                        target = node
                        print(node, node["data"]["label"])
                        return json.dumps(node["data"], indent= 2)
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
