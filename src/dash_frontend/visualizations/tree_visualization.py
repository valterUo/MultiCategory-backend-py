import dash_cytoscape as cyto
import dash_html_components as html
from dash.dependencies import Input, Output
import json
import uuid
import dash
from dash_frontend.server import app
from supportive_functions.xml_to_dict import XmlDictConfig, XmlListConfig
from supportive_functions.json_manipulations import decode_shelve_to_json
from dash.exceptions import PreventUpdate
tree = None

"""
Cytoscape nodes {'data': {'id': 'one', 'label': 'Node 1'}, 'position': {'x': 50, 'y': 50}}
Cytoscape edges {'data': {'source': 'one', 'target': 'two', 'label': 'Node 1 to 2'}}
"""


def tree_to_cytoscape(visualized_object):
    nodes, edges, root_ids = dict_to_tree(visualized_object)
    cyto_fig = html.Div(children=[cyto.Cytoscape(
        id='cytoscape-tree-result',
        layout={
            'name': 'breadthfirst',
            'roots': root_ids
        },
        style={'width': '100%', 'margin': '0 auto',
               'height': '900px', 'backgroundColor': '#f8f7ed'},
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
    ), html.Br(), html.Pre(id='output-tree-as-json', style={'display': 'none'}), html.Br(),
        html.Button(id="show-json", children="SHOW TREE AS JSON")])
    return cyto_fig


@app.callback(
    [Output("output-tree-as-json", "children"),
     Output("output-tree-as-json", 'style'), Output("show-json", "style")],
    [Input("show-json", "n_clicks")],
)
def show_whole_tree(button_click):
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "show-json":
            return json.dumps(decode_shelve_to_json(None, tree), indent=2), {'display': 'block', 'border': 'thin lightgrey solid', 'overflowX': 'scroll', 'width': '100%'}, {'display': 'none'}
    else:
        raise PreventUpdate


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


def dict_to_tree(visualized_object):
    T = visualized_object.get_collection().get_tree()
    global tree
    tree = T
    nodes, edges, root_ids = [], [], []
    # We assume that T is not a list of objects but dictionary of objects
    for key in T:
        tag_id = str(uuid.uuid4())
        root_ids.append(tag_id)
        nodes.append({'data': {'id': tag_id, 'label': key}})
        walk_tree(tag_id, key, T, nodes, edges)
    return nodes, edges, root_ids
