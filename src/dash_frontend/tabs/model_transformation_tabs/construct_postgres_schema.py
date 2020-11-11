from dash.exceptions import PreventUpdate
from dash_html_components.Button import Button
import networkx as nx
import dash_cytoscape as cyto
import dash_html_components as html
from dash.dependencies import Input, Output
from dash_frontend.server import app
from supportive_functions.json_manipulations import decode_to_json
graph = None


def construct_postgres_schema(rel_db):
    res = rel_schema_to_nx_graph(rel_db)
    return schema_nx_grah_to_cytoscape(res)


def rel_schema_to_nx_graph(rel_db):
    G = nx.DiGraph()
    G.graph["title"] = rel_db.get_name()
    schema = rel_db.get_schema()
    nodes = []
    for key in schema:
        nodes.append(
            (key, {"name": key, "attributes": ", ".join(schema[key])}))
    G.add_nodes_from(nodes)
    print(G)
    default_edges = rel_db.return_all_pk_fk_contrainsts()
    edges = []
    for e in default_edges:
        print(e, default_edges[e])
        for fk in default_edges[e]:
            if "target_table" in default_edges[e][fk].keys():
                edges.append((default_edges[e][fk]["target_table"], e, {
                             "fk": fk, "pk": default_edges[e][fk]["primary_key_in_target_table"]}))
    G.add_edges_from(edges)
    return G


def parse_cytoscape_nodes_edges(G):
    nodes, edges = [], []
    for node in G.nodes.data():
        nodes.append(
            {'data': {'id': node[0], 'label': str(next(iter(node[1].values())))}})
    for edge in G.edges.data():
        edges.append(
            {'data': {'source': edge[0], 'target': edge[1], 'label': ""}})
    return nodes, edges


def schema_nx_grah_to_cytoscape(g):
    global graph
    graph = g
    nodes, edges = parse_cytoscape_nodes_edges(graph)
    cyto_fig = html.Div(children=[
        cyto.Cytoscape(
            id='rel-schema-cytoscape-result',
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
                        'color': 'black',
                        'curve-style': 'bezier',
                        'target-arrow-shape': 'triangle'
                    }
                }
            ]
        ),
        html.Pre(id='rel-schema-cytoscape-tapNodeData-output', style={
            'border': 'thin lightgrey solid', 'margin': '0 auto',
            'overflowX': 'scroll', 'width': '90%'}),
        html.Pre(id='rel-schema-cytoscape-tapEdgeData-output', style={
            'border': 'thin lightgrey solid', 'margin': '0 auto',
            'overflowX': 'scroll', 'width': '90%'})])
    return cyto_fig


@app.callback(Output('rel-schema-cytoscape-tapNodeData-output', 'children'),
              [Input('rel-schema-cytoscape-result', 'tapNodeData')])
def displayTapNodeData(data):
    print(data)
    if data != None:
        for node in graph.nodes.data():
            if node[0] == data["id"]:
                return decode_to_json(node[1])
    else:
        return "Select node"


@app.callback(Output('rel-schema-cytoscape-tapEdgeData-output', 'children'),
              [Input('rel-schema-cytoscape-result', 'tapEdgeData')])
def displayTapEdgeData(data):
    print(data)
    if data != None:
        for edge in graph.edges.data():
            if data["source"] == edge[0] and data["target"] == edge[1]:
                return "You clicked the edge between " + data['source'].upper() + " and " + data['target'].upper() + " containing information: " + decode_to_json(edge[2])
    else:
        return "Select edge"