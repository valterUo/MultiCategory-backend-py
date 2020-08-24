import dash
import dash_core_components as dcc
import dash_html_components as html

datasets = [
    {'label': 'E-commerce dataset', 'value': 'ecommerce'},
    {'label': 'Patent dataset', 'value': 'patent'},
    {'label': 'Online market place', 'value': 'market_place'},
    {'label': 'Unibench small dataset', 'value': 'unibench_small'},
    {'label': 'University dataset', 'value': 'university'},
    {'label': 'Person dataset', 'value': 'person'},
    {'label': 'Film dataset', 'value': 'film'}
]

def define_settings_tab():
    return dcc.Tab(
        id="Settings-tab",
        label="Database Settings",
        value="tab1",
        className="custom-tab",
        selected_className="custom-tab--selected",
    )

def build_settings_tab(current_state):
    return [
    html.Div(
        id="set-specs-intro-container",
        children=[html.P(
            "Select the demo dataset. The default dataset is the e-commerce dataset."
        ),
            dcc.Dropdown(
                id="metric-select-dropdown",
                options=datasets,
                value = current_state["value"]
        ),
    ]
    ),
]
        # html.Div(
        #     id="settings-menu",
        #     children=[
        #         html.Div(
        #             id="metric-select-menu",
        #             # className='five columns',
        #             children=[
        #                 html.Label(id="metric-select-title",
        #                            children="Select dataset"),
        #                 html.Br(),
        #                 dcc.Dropdown(
        #                     id="metric-select-dropdown",
        #                     options=[
        #                         {'label': 'Coke', 'value': 'COKE'},
        #                         {'label': 'Tesla', 'value': 'TSLA'},
        #                         {'label': 'Apple', 'value': 'AAPL'}
        #                     ],
        #                     value='COKE'
        #                 ),
        #             ],
        #         ),
                # html.Div(
                #     id="value-setter-menu",
                #     # className='six columns',
                #     children=[
                #         html.Div(id="value-setter-panel"),
                #         html.Br(),
                #         html.Div(
                #             id="button-div",
                #             children=[
                #                 html.Button(
                #                     "Update", id="value-setter-set-btn"),
                #                 html.Button(
                #                     "View current setup",
                #                     id="value-setter-view-btn",
                #                     n_clicks=0,
                #                 ),
                #             ],
                #         ),
                #         html.Div(
                #             id="value-setter-view-output", className="output-datatable"
                #         ),
                #     ],
                # ),
        #     ],
        # ),
