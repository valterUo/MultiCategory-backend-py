import dash
import dash_core_components as dcc
import dash_html_components as html

def query_tab():
    return dcc.Tab(
        id="Query-tab",
        label="Queries",
        value="tab3",
        className="custom-tab",
        selected_className="custom-tab--selected",
    )

def build_query_tab():
    return [
    # Manually select metrics
    html.Div(
        id="set-specs-intro-container",
        # className='twelve columns',
        children=html.P(
            "Use historical control limits to establish a benchmark, or set new values."
        ),
    ),
    # html.Div(
    #     id="settings-menu",
    #     children=[
    #         html.Div(
    #             id="metric-select-menu",
    #             # className='five columns',
    #             children=[
    #                 html.Label(id="metric-select-title", children="Select Metrics"),
    #                 html.Br(),
    #                 dcc.Dropdown(
    #                     id="metric-select-dropdown",
    #                     options=list(
    #                         {"label": param, "value": param} for param in params[1:]
    #                     ),
    #                     value=params[1],
    #                 ),
    #             ],
    #         ),
    #         html.Div(
    #             id="value-setter-menu",
    #             # className='six columns',
    #             children=[
    #                 html.Div(id="value-setter-panel"),
    #                 html.Br(),
    #                 html.Div(
    #                     id="button-div",
    #                     children=[
    #                         html.Button("Update", id="value-setter-set-btn"),
    #                         html.Button(
    #                             "View current setup",
    #                             id="value-setter-view-btn",
    #                             n_clicks=0,
    #                         ),
    #                     ],
    #                 ),
    #                 html.Div(
    #                     id="value-setter-view-output", className="output-datatable"
    #                 ),
    #             ],
    #         ),
    #     ],
    # ),
]