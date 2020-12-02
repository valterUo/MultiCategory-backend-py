import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import os
from dash_frontend.server import app
from dash.exceptions import PreventUpdate
from multicategory.initialize_multicategory import multicategory
dirname = os.path.dirname(__file__)
full_config_file_path = os.path.join(
    dirname, "..//..//external_database_connections//config//databases.ini")


def define_settings_tab():
    return dcc.Tab(
        id="Settings-tab",
        label="Database Settings",
        value="tab1",
        className="custom-tab",
        selected_className="custom-tab--selected",
    )


def build_settings_tab():
    dbs = multicategory.get_multi_model_db_names_for_dropdown()
    selected_db = multicategory.get_selected_multi_model_database().get_name()
    print("First selection: ", selected_db)
    return [
        html.Div(
            id="set-specs-intro-container",
            children=[html.H5(
                "Select the preinstalled multi-model database. The default database is the e-commerce database."
            ),
                dcc.Dropdown(
                id="select-multi-model-database",
                options=dbs,
                value=selected_db
            ),
                html.Br(),
                build_external_database_textarea_connection()
            ]
        ),
    ]


@app.callback(
    Output("selected-dataset-banner-parent", "children"),
    [Input("select-multi-model-database", "value")],
)
def handle_dataset_selection(db_name):
    db = multicategory.get_multi_model_db(db_name)
    print(db_name, db.is_available())
    if db.is_available():
        multicategory.change_to_multi_model_db(db_name)
        return html.P("Selected database: " + db_name)
    else:
        return html.P("The selected database " + db_name + " is not currently available.")


def build_external_database_textarea_connection():
    content = ""
    with open(full_config_file_path, 'r') as file:
        content = file.read()
    return html.Div([html.H5("External database connection information"),
                     dcc.Textarea(
        id='textarea-state-config',
        value=content,
        style={'width': '100%', 'height': 300, "fontFamily": "monospace"},
    ),
        html.Button('Update config file',
                    id='config-textarea-state-button', n_clicks=0),
        html.Br(),
        html.Div(id="config-file-update-notification")
    ])


@app.callback(
    [Output('textarea-state-config', 'value'),
     Output("config-file-update-notification", "children")],
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
            return value, html.P("The config file updated succesfully!", style={'color': 'green'})
        else:
            return value, html.P("The config file is not updated!", style={'color': 'red'})
    else:
        raise PreventUpdate
