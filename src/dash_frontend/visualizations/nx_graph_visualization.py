import dash_cytoscape as cyto
import networkx as nx
import dash_core_components as dcc
from dash_frontend.state.initialize_demo_state import multi_model_join_results
import dash_html_components as html
from dash.dependencies import Input, Output
import json
from dash_frontend.server import app

"""
Cytoscape nodes {'data': {'id': 'one', 'label': 'Node 1'}, 'position': {'x': 50, 'y': 50}}
Cytoscape edges {'data': {'source': 'one', 'target': 'two', 'label': 'Node 1 to 2'}}
"""

def general_nx_grah_to_cytoscape():
    result = multi_model_join_results.get_current_state()
    G = result.get_collection().get_graph()
    nodes, edges = [], []
    for node in G.nodes.data():
        print(node[1])
        nodes.append({'data': {'id': node[0], 'label': str(next(iter(node[1].values())))}})
    for edge in G.edges.data():
        print(edge)
        edges.append(
            {'data': {'source': edge[0], 'target': edge[1], 'label': ""}})
    cyto_fig = html.Div( children = [cyto.Cytoscape(
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
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll', 'width': '90%' }),
        html.Pre(id='cytoscape-tapEdgeData-output', style={
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll', 'width': '90%' })])
    return cyto_fig

@app.callback(Output('cytoscape-tapNodeData-output', 'children'),
              [Input('cytoscape-result', 'tapNodeData')])
def displayTapNodeData(data):
    if data != None:
        result = multi_model_join_results.get_current_state()
        G = result.get_collection().get_graph()
        for node in G.nodes.data():
            if node[0] == data["id"]:
                return decode_to_json(node[1])
    else:
        return "Select node"

def decode_to_json(old_dict):
    new_dict = dict()
    for key in old_dict:
        try:
            new_dict[key] = old_dict[key].decode("utf-8")
        except:
            new_dict[key] = old_dict[key]
    return json.dumps(new_dict, indent=2)

@app.callback(Output('cytoscape-tapEdgeData-output', 'children'),
                  [Input('cytoscape-result', 'tapEdgeData')])
def displayTapEdgeData(data):
    if data != None:
        result = multi_model_join_results.get_current_state()
        G = result.get_collection().get_graph()
        for edge in G.edges.data():
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