import dash_cytoscape as cyto
import dash_html_components as html
from dash.dependencies import Input, Output
from dash_frontend.server import app
from supportive_functions.json_manipulations import decode_to_json
graph = None
"""
Cytoscape nodes {'data': {'id': 'one', 'label': 'Node 1'}, 'position': {'x': 50, 'y': 50}}
Cytoscape edges {'data': {'source': 'one', 'target': 'two', 'label': 'Node 1 to 2'}}
"""


def parse_cytoscape_nodes_edges(G):
    nodes, edges = [], []
    for node in G.nodes.data():
        nodes.append(
            {'data': {'id': node[0], 'label': str(next(iter(node[1].values())))}})
    for edge in G.edges.data():
        edges.append(
            {'data': {'source': edge[0], 'target': edge[1], 'label': ""}})
    return nodes, edges


def general_nx_grah_to_cytoscape(visualized_object):
    global graph
    graph = visualized_object.get_collection().get_graph()
    nodes, edges = parse_cytoscape_nodes_edges(graph)
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
                    #'content': 'data(label)',
                    'color': 'black',
                    'curve-style': 'bezier',
                    'target-arrow-shape': 'triangle'
                }
            }
        ]
    ), html.Pre(id='cytoscape-tapNodeData-output', style={
        'border': 'thin lightgrey solid', 'margin': '0 auto',
        'overflowX': 'scroll', 'width': '90%'}),
        html.Pre(id='cytoscape-tapEdgeData-output', style={
            'border': 'thin lightgrey solid', 'margin': '0 auto',
            'overflowX': 'scroll', 'width': '90%'})])
    return cyto_fig


@app.callback(Output('cytoscape-tapNodeData-output', 'children'),
              [Input('cytoscape-result', 'tapNodeData')])
def displayTapNodeData(data):
    if data != None:
        for node in graph.nodes.data():
            if node[0] == data["id"]:
                return decode_to_json(node[1])
    else:
        return "Select node"


@app.callback(Output('cytoscape-tapEdgeData-output', 'children'),
              [Input('cytoscape-result', 'tapEdgeData')])
def displayTapEdgeData(data):
    if data != None:
        for edge in graph.edges.data():
            if data["source"] == edge[0] and data["target"] == edge[1]:
                return "You clicked the edge between " + data['source'].upper() + " and " + data['target'].upper() + " containing information: " + decode_to_json(edge[2])
    else:
        return "Select edge"


def nx_grah_to_cytoscape(G):
    nodes, edges = [], []
    for node in G.nodes.data():
        nodes.append({'data': {'id': node[0], 'label': node[1]["label"]}})
    for edge in G.edges.data():
        edges.append(
            {'data': {'source': edge[0], 'target': edge[1], 'label': edge[2]["label"]}})
    cyto_fig = cyto.Cytoscape(
        id='cytoscape-' + G.graph["title"],
        layout={'name': 'circle'},
        style={'width': '90%', 'margin': '0 auto',
               'height': '450px', 'backgroundColor': '#f8f7ed'},
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
    )
    return cyto_fig
