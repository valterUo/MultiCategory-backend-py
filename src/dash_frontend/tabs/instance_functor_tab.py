import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
import networkx as nx
import plotly.graph_objects as go
G = nx.random_geometric_graph(10, 0.5)

"""
Cytoscape nodes {'data': {'id': 'one', 'label': 'Node 1'}, 'position': {'x': 50, 'y': 50}}
Cytoscape edges {'data': {'source': 'one', 'target': 'two', 'label': 'Node 1 to 2'}}
"""

def define_instance_functor_tab():
    return dcc.Tab(
        id="Instance-tab",
        label="Instance Functor",
        value="tab2",
        className="custom-tab",
        selected_className="custom-tab--selected",
    )


def build_instance_functor_tab(database, mode = "cytoscape"):
    G = database["db"].get_instance_category_nx_graph()
    #F = database["db"].get_schema_category_nx_graph()
    instance_fig = nx_grah_to_cytoscape(G)
    #schema_fig = nx_grah_to_cytoscape(F)
    return [
        html.Div(id="instance-functor-parent",
                 children=[
                     html.Div(
                         id="set-specs-intro-container",
                         children=[html.H5(
                             "The visualization of the schema and instance categories."), ]
                     ),
                     html.Div(
                         id="schema-category",
                         children=[ html.H6("Schema category"), ]#schema_fig]
                     ),
                     html.Div(
                         id="instance-category",
                         children=[html.H6("Instance category"), instance_fig]
                     ), ])
    ]

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
                title='<br>' + "title", #G.graph["title"],
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=5,l=5,r=5,t=5),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
    return dcc.Graph(figure = fig)

def nx_grah_to_cytoscape(G):
    nodes, edges = [], []
    for node in G.nodes.data():
        nodes.append({'data': {'id': node[0], 'label': node[1]["label"]}})
    for edge in G.edges.data():
        edges.append({'data': {'source': edge[0], 'target': edge[1], 'label': edge[2]["label"]}})
    cyto_fig = cyto.Cytoscape(
        id='cytoscape-' + G.graph["title"],
        layout={'name': 'circle'},
        style={'width': '100%', 'height': '500px', 'backgroundColor': '#f8f7ed'},
        elements= nodes + edges,
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