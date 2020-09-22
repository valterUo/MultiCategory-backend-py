import dash_core_components as dcc
import dash_html_components as html


def render_return_attribute_input(domain_model, query_state):
    target_model = None
    if len(query_state) > 0:
        previous_block = query_state[-1]
        target_model = previous_block["target_model"]

    graph_query_attribute_style = {'display': 'none'}
    query_attribute_style = {'display': 'block'}
    if domain_model == "graph" or target_model == "graph":
        graph_query_attribute_style = {'display': 'block'}
        query_attribute_style = {'display': 'none'}

    return html.Div(id="main-query-attiribute-container", children=[html.Div(id="graph-query-attribute-container", style=graph_query_attribute_style, children=html.Div([
        html.Label([
            "Vertex attributes",
            dcc.Input(
                   id="return-attribute-vertex-input",
                   type="text",
                   value="",
                   placeholder="return attributes",
                   style={'width': '90%',
                          "display": "block"},
                   )]),
        html.Br(),
        html.Label([
            "Possible attributes for vertices", html.Br(),
            dcc.Dropdown(
                   id="return-attribute-vertex-dropdown",
                   style={'width': '90%',
                          "display": "block"},
                   options=[],
                   multi=True
                   )
        ]
        ),
        html.Br(),
        html.Label(["Edge attributes",
                    dcc.Input(
                        id="return-attribute-edge-input",
                        type="text",
                        value="",
                        placeholder="return attributes",
                        style={'width': '90%',
                               "display": "block"},
                    )]),
        html.Br(),
        html.Label([
            "Possible attributes for edges", html.Br(),
            dcc.Dropdown(
                   id="return-attribute-edge-dropdown",
                   style={'width': '90%',
                          "display": "block"},
                   options=[],
                   multi=True
                   )
        ]
        )
    ])),
        html.Div(
        html.Div(id="query-attribute-container", style=query_attribute_style, children=[
            html.Label([
                       "Input return attributes for this block",
                       html.Br(),
                       dcc.Input(
                           id="return-attributes-input",
                           type="text",
                           value="",
                           placeholder="return attributes",
                           style={'width': '90%',
                                  "display": "block"},
                       )]), html.Br(),
            html.Label([
                       "Possible attributes", html.Br(),
                       dcc.Dropdown(
                           id="return-attribute-dropdown",
                           style={'width': '90%',
                                  "display": "block"},
                           options=[],
                           multi=True
                       )
                       ])
        ])
    )])
