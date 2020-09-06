import dash_cytoscape as cyto
import networkx as nx
import dash_core_components as dcc

"""
Cytoscape nodes {'data': {'id': 'one', 'label': 'Node 1'}, 'position': {'x': 50, 'y': 50}}
Cytoscape edges {'data': {'source': 'one', 'target': 'two', 'label': 'Node 1 to 2'}}
"""

def general_nx_grah_to_cytoscape(G):
    nodes, edges = [], []
    for node in G.nodes.data():
        print(node[1])
        nodes.append({'data': {'id': node[0], 'label': str(node[1])}})
    for edge in G.edges.data():
        print(edge)
        edges.append(
            {'data': {'source': edge[0], 'target': edge[1], 'label': "label"}})
    cyto_fig = cyto.Cytoscape(
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
    )
    return cyto_fig


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

## This function does not work currently but it draws nice graphs. I do not understand how Scatter class works.


def nx_graph_to_plotly(G):
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_y.append(y0)
        edge_y.append(y1)

    print(edge_x)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2.0, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x, node_y = [], []
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(size=20)
        #     showscale=True,
        #     # colorscale options
        #     #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
        #     #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
        #     #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
        #     colorscale='Electric',
        #     reversescale=True,
        #     color=[],
        #     size=20,
        #     colorbar=dict(
        #         thickness=15,
        #         title='Node Connections',
        #         xanchor='left',
        #         titleside='right'
        #     ),
        #     line_width=2)
    )

    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append('# of connections: '+str(len(adjacencies[1])))

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
        title='<br>' + "title",  # G.graph["title"],
        titlefont_size=16,
        showlegend=False,
        hovermode='closest',
        margin=dict(b=5, l=5, r=5, t=5),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
    )
    return dcc.Graph(figure=fig)
