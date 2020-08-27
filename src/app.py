import os
import pathlib

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import plotly.graph_objs as go
import dash_daq as daq
from dash_frontend.server import app
import pandas as pd

from dash_frontend.tabs.settings_tab import define_settings_tab, build_settings_tab
from dash_frontend.tabs.instance_functor_tab import define_instance_functor_tab, build_instance_functor_tab
from dash_frontend.tabs.query_tab import query_tab, build_query_tab
from dash_frontend.tabs.multi_model_join_tab import multi_model_join_tab, build_multi_model_join_tab
from dash_frontend.modal.modal import generate_modal
from dash_frontend.state.initialize_demo_state import state

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
            html.Div(id = "selected-dataset-banner-parent", children = html.P("Selected database: " + state.get_current_state()["label"])),
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
        return build_settings_tab(state)
    elif tab_switch == "tab3":
        return build_query_tab()
    elif tab_switch == "tab4":
        return build_multi_model_join_tab(state)
    return build_instance_functor_tab(state)


# ===== Callbacks to update values based on store data and dropdown selection =====
@app.callback(
    output= Output("selected-dataset-banner-parent", "children"),
    inputs=[Input("metric-select-dropdown", "value")],
)
def handle_dataset_selection(ds_select):
    database = state.get_possible_states()[ds_select]
    if database["available"]:
        state.change_state(ds_select)
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
