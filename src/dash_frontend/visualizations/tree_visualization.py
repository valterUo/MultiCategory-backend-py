import dash_cytoscape as cyto
import networkx as nx
import dash_core_components as dcc
from dash_frontend.state.initialize_demo_state import multi_model_join_results, state
import dash_html_components as html
from dash.dependencies import Input, Output
import json
from dash_frontend.server import app
import uuid
from supportive_functions.xml_to_dict import XmlDictConfig, XmlListConfig

"""
Cytoscape nodes {'data': {'id': 'one', 'label': 'Node 1'}, 'position': {'x': 50, 'y': 50}}
Cytoscape edges {'data': {'source': 'one', 'target': 'two', 'label': 'Node 1 to 2'}}
"""

def tree_to_cytoscape():
    nodes, edges, root_ids = dict_to_tree()
    cyto_fig = html.Div( children = [cyto.Cytoscape(
        id='cytoscape-tree-result',
        layout={
                'name': 'breadthfirst',
                'roots': root_ids
            },
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
    ), html.Pre(id='cytoscape-tapNodeData-output-tree', style={
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll', 'width': '90%' })])
    return cyto_fig

# @app.callback(Output('cytoscape-tapNodeData-output-tree', 'children'),
#               [Input('cytoscape-tree-result', 'tapNodeData')])
# def displayTapNodeData(data):
#     if data != None:
#         result = multi_model_join_results.get_current_state()
#         G = result.get_collection().get_tree()
#         for node in G.nodes.data():
#             if node[0] == data["id"]:
#                 return decode_to_json(node[1])
#     else:
#         return "Select node"

def decode_to_json(old_dict):
    new_dict = dict()
    for key in old_dict:
        try:
            new_dict[key] = old_dict[key].decode("utf-8")
        except:
            new_dict[key] = old_dict[key]
    return json.dumps(new_dict, indent=2)

def walk_tree(previous_id, root, tree, nodes, edges):
    if type(root) == dict or type(root) == XmlDictConfig:
        for key in root:
            tag_id = str(uuid.uuid4())
            nodes.append({'data': {'id': tag_id, 'label': key}})
            edges.append({'data': {'source': previous_id, 'target': tag_id}})
            walk_tree(tag_id, root[key], tree, nodes, edges)
    elif type(root) == list or type(root) == XmlListConfig:
        for elem in root:
            tag_id = str(uuid.uuid4())
            nodes.append({'data': {'id': tag_id, 'label': "list item"}})
            edges.append({'data': {'source': previous_id, 'target': tag_id}})
            walk_tree(tag_id, elem, tree, nodes, edges)
    else:
        tag_id = str(uuid.uuid4())
        nodes.append({'data': {'id': tag_id, 'label': str(root)}})
        edges.append({'data': {'source': previous_id, 'target': tag_id}})
        try:
            walk_tree(tag_id, tree[root], tree, nodes, edges)
        except:
            pass


def dict_to_tree():
    result = multi_model_join_results.get_current_state()
    T = result.get_collection().get_tree()
    nodes, edges, root_ids = [], [], []
    # We assume that T is not a list of objects but dictionary of objects
    for key in T:
        tag_id = str(uuid.uuid4())
        root_ids.append(tag_id)
        nodes.append({'data': {'id': tag_id, 'label': key}})
        walk_tree(tag_id, key, T, nodes, edges)
    return nodes, edges, root_ids