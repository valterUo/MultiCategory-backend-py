import networkx as nx
import dash_cytoscape as cyto
import dash_core_components as dcc
from dash_frontend.state.initialize_demo_state import multi_model_join_results
import dash_html_components as html
from dash.dependencies import Input, Output
from dash_frontend.server import app

def parse_cytoscape_nodes_edges(G):
    nodes, edges = [], []
    for node in G.nodes.data():
        print(node[1])
        nodes.append(
            {'data': {'id': node[0], 'label': node[1]["label"]}})
    for edge in G.edges.data():
        print(edge)
        edges.append(
            {'data': {'source': edge[0], 'target': edge[1], 'label': edge[2]["label"]}})
    return nodes, edges


def model_category_nx_grah_to_cytoscape():
    join_result = multi_model_join_results.get_current_state()
    model_category_join = join_result.get_model_category_join()
    G = model_category_join.get_commutative_triangle()
    nodes, edges = parse_cytoscape_nodes_edges(G)

    cyto_fig = html.Div(children=[cyto.Cytoscape(
        id='cytoscape-model-category',
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
    ), 
    # html.Pre(id='cytoscape-tapNodeData-output', style={
    #     'border': 'thin lightgrey solid',
    #     'overflowX': 'scroll', 'width': '90%'}),
    #     html.Pre(id='cytoscape-tapEdgeData-output', style={
    #         'border': 'thin lightgrey solid',
    #         'overflowX': 'scroll', 'width': '90%'})
    ])
    return cyto_fig