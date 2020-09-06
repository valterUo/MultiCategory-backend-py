import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import os
from dash_frontend.server import app
from dash.exceptions import PreventUpdate
dirname = os.path.dirname(__file__)
full_config_file_path = os.path.join(dirname, "..\\..\\external_database_connections\\config\\databases.ini")

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


def build_settings_tab(state):
    current_state = state.get_current_state()
    return [
        html.Div(
            id="set-specs-intro-container",
            children=[html.H5(
                "Select the demo dataset. The default dataset is the e-commerce dataset."
            ),
                dcc.Dropdown(
                id="metric-select-dropdown",
                options=datasets,
                value=current_state["value"]
            ),
            html.Br(),
            build_external_database_textarea_connection()
            ]
        ),
    ]

def build_external_database_textarea_connection():
    content = ""
    with open(full_config_file_path, 'r') as file:
        content = file.read()
    return html.Div([ html.H5("External database connection information"),
        dcc.Textarea(
            id='textarea-state-config',
            value = content,
            style={'width': '100%', 'height': 300, "fontFamily": "monospace"},
        ),
        html.Button('Update config file', id='config-textarea-state-button', n_clicks=0)
    ])

@app.callback(
    Output('textarea-state-config', 'value'),
    [Input('config-textarea-state-button', 'n_clicks')],
    [State('textarea-state-config', 'value')]
)
def update_output(n_clicks, value):
    ctx = dash.callback_context
    prop_id = ""
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if prop_id == "config-textarea-state-button":
        if len(value) > 10:
            with open(full_config_file_path, 'w') as file:
                file.write(value)
            return value
        else:
            return value
    else:
        raise PreventUpdate
