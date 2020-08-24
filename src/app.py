import os
import pathlib

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import plotly.graph_objs as go
import dash_daq as daq

import pandas as pd

from dash_frontend.tabs.settings_tab import define_settings_tab, build_settings_tab
from dash_frontend.tabs.instance_functor_tab import define_instance_functor_tab, build_instance_functor_tab
from dash_frontend.tabs.query_tab import query_tab, build_query_tab
from dash_frontend.tabs.multi_model_join_tab import multi_model_join_tab, build_multi_model_join_tab
from dash_frontend.modal.modal import generate_modal

## Pre-defined databases
from initialization_of_demo_databases.initialize_ecommerce import ECommerceMultiModelDatabase
from initialization_of_demo_databases.initialize_patent_data import PatentMultiModelDatabase

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server
app.config["suppress_callback_exceptions"] = True

## Initially the E-commerce database is selected.
selected_database = "ecommerce"

def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H5("MultiCategory v2.0"),
                    html.H6("Applying category theory to multi-model database management systems, query processing and model transformations"),
                ],
            ),
            html.Div(id = "selected-dataset-banner-parent", children = html.P("Selected database: " + state_dict[selected_database]["label"])),
            html.Div(
                id="banner-logo",
                children=[
                    html.Button(
                        id="learn-more-button", children="LEARN MORE", n_clicks=0
                    ),
                    html.Img(id="logo", src=app.get_asset_url("UDBMSTransparentLogo.png")),
                ],
            ),
        ],
    )

def build_tabs():
    print("Building tabs")
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="tab2",
                className="custom-tabs",
                children=[
                    define_settings_tab(),
                    define_instance_functor_tab(),
                    query_tab(),
                    multi_model_join_tab(),
                ],
            ),
        ],
    )


def init_databases():
    state = {
        "ecommerce": {'label': 'E-commerce dataset', 'value': 'ecommerce', 'available': True, 'db': ECommerceMultiModelDatabase().get_multi_model_db()},
        "patent": {'label': 'Patent dataset', 'value': 'patent', 'available': True, 'db': PatentMultiModelDatabase().get_multi_model_db()},
        "market_place": {'label': 'Online market place', 'value': 'market_place', 'available': False, 'db': None},
        "unibench_small": {'label': 'Unibench small dataset', 'value': 'unibench_small', 'available': False,'db': None},
        "university": {'label': 'University dataset', 'value': 'university', 'available': False, 'db': None},
        "person": {'label': 'Person dataset', 'value': 'person', 'available': False, 'db': None},
        "film": {'label': 'Film dataset', 'value': 'film', 'available': False, 'db': None}
    }
    return state

state_dict = init_databases()

app.layout = html.Div(
    id="big-app-container",
    children=[
        build_banner(),
        html.Div(
            id="app-container",
            children=[
                build_tabs(),
                # Main app
                html.Div(id="app-content"),
            ],
        ),
        generate_modal(),
    ],
)

# ======= Callbacks for changing tabs =======
@app.callback(
    [Output("app-content", "children")],
    [Input("app-tabs", "value")],
)
def render_tab_content(tab_switch):
    if tab_switch == "tab1":
        return build_settings_tab(state_dict[selected_database])
    elif tab_switch == "tab3":
        return build_query_tab()
    elif tab_switch == "tab4":
        return build_multi_model_join_tab()
    return build_instance_functor_tab(state_dict[selected_database])


# ===== Callbacks to update values based on store data and dropdown selection =====
@app.callback(
    output= Output("selected-dataset-banner-parent", "children"),
    inputs=[Input("metric-select-dropdown", "value")],
)
def handle_dataset_selection(ds_select):
    database = state_dict[ds_select]
    if database["available"]:
        global selected_database
        selected_database = ds_select
        return html.P("Selected database: " + database["label"])
    else:
        return html.P("The selected database " + database["label"] + " is not currently available.")

    
# ======= Callbacks for modal popup =======
@app.callback(
    Output("markdown", "style"),
    [Input("learn-more-button", "n_clicks"), Input("markdown_close", "n_clicks")],
)
def update_click_output(button_click, close_click):
    ctx = dash.callback_context

    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "learn-more-button":
            return {"display": "block"}
    return {"display": "none"}

# Running the server
if __name__ == "__main__":
    app.run_server(port=8050, debug=True, dev_tools_ui=False, dev_tools_props_check=True)
