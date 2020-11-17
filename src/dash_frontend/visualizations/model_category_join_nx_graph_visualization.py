import dash_cytoscape as cyto
import dash_html_components as html


def parse_cytoscape_nodes_edges(G):
    nodes, edges = [], []
    for node in G.nodes.data():
        nodes.append(
            {'data': {'id': node[0], 'label': node[1]["label"]}})
    for edge in G.edges.data():
        edges.append(
            {'data': {'source': edge[0], 'target': edge[1], 'label': edge[2]["label"]}})
    return nodes, edges


def model_category_nx_grah_to_cytoscape(join_result):
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
    ])
    return cyto_fig
