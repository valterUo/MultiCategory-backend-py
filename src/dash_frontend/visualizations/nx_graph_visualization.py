import dash_cytoscape as cyto
import dash_html_components as html
from dash.dependencies import Input, Output
from networkx.generators import expanders
from dash_frontend.server import app
from supportive_functions.json_manipulations import decode_to_json
from networkx import DiGraph
import networkx as nx
import itertools
graph = None
"""
Cytoscape nodes {'data': {'id': 'one', 'label': 'Node 1'}, 'position': {'x': 50, 'y': 50}}
Cytoscape edges {'data': {'source': 'one', 'target': 'two', 'label': 'Node 1 to 2'}}
"""


def parse_cytoscape_nodes_edges(G):
    print(G)
    print(nx.number_of_nodes(G))
    print(nx.number_of_edges(G))
    nodes, edges = [], []
    for node in G.nodes.data():
        try:
            nodes.append(
                {'data': {'id': node[0], 'label': str(next(iter(node[1].values())))}})
        except:
            nodes.append({'data': {'id': node[0], 'label': node[0]}})
    for edge in G.edges.data():
        edges.append(
            {'data': {'source': edge[0], 'target': edge[1], 'label': ""}})
    return nodes, edges


def general_nx_grah_to_cytoscape(visualized_object):
    global graph
    message = ""
    print(type(visualized_object))
    if type(visualized_object) == DiGraph:
        graph = visualized_object
    else:
        graph = visualized_object.get_collection().get_graph()
        print("number of nodes in the graph: ", nx.number_of_nodes(graph))
        print("number of edges in the graph: ", nx.number_of_edges(graph))
        if nx.number_of_nodes(graph) > 30:
            message = "The graph has " + str(nx.number_of_edges(graph)) + " edges and " +  str(nx.number_of_nodes(graph)) + " nodes. The subgraph induced by first 50 nodes is shown."
            selected_nodes = list(itertools.islice(graph.nodes, 0, 30))
            print(selected_nodes)
            graph = graph.subgraph(selected_nodes)
            
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
            'overflowX': 'scroll', 'width': '90%'}),
        html.Div(id = "notification", children = [message])])
    return cyto_fig


@app.callback(Output('cytoscape-tapNodeData-output', 'children'),
              [Input('cytoscape-result', 'tapNodeData')])
def displayTapNodeData(data):
    if data != None:
        for node in graph.nodes.data():
            if node[0] == data["id"]:
                if len(node[1]) == 0:
                    return node[0]
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
