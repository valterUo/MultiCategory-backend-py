import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash_frontend.server import app

from dash_frontend.tabs.settings_tab import define_settings_tab, build_settings_tab
from dash_frontend.tabs.instance_functor_tab import define_instance_functor_tab, build_instance_functor_tab
from dash_frontend.tabs.query_tabs.query_tab import query_tabs, build_query_tabs
from dash_frontend.tabs.multi_model_join_tab import multi_model_join_tab, build_multi_model_join_tab
from dash_frontend.tabs.model_transformation_tabs.model_transformation_tab import transformation_tabs, build_transformation_tabs
from dash_frontend.tabs.result_tab import result_tab, build_result_tab
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
                    html.H6(
                        "Applying category theory to multi-model database management systems, query processing and model transformations"),
                ],
            ),
            html.Div(id="selected-dataset-banner-parent", children=html.P(
                "Selected database: " + state.get_current_state()["label"])),
            html.Div(
                id="banner-logo",
                children=[
                    html.Button(
                        id="learn-more-button", children="LEARN MORE", n_clicks=0
                    ),
                    html.Img(id="logo", src=app.get_asset_url(
                        "favicon.png")),
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
                    query_tabs(),
                    multi_model_join_tab(),
                    transformation_tabs(),
                    result_tab(),
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
        generate_modal()
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
        return build_query_tabs()
    elif tab_switch == "tab4":
        return build_multi_model_join_tab()
    elif tab_switch == "tab5":
        return build_transformation_tabs()
    elif tab_switch == "tab6":
        return build_result_tab()
    return build_instance_functor_tab()


# ===== Callbacks to update values based on store data and dropdown selection =====
@app.callback(
    Output("selected-dataset-banner-parent", "children"),
    [Input("metric-select-dropdown", "value")],
)
def handle_dataset_selection(ds_select):
    if ds_select != None:
        database = state.get_possible_states()[ds_select]
        if database["available"]:
            state.change_state(ds_select)
            return html.P("Selected database: " + database["label"])
        else:
            return html.P("The selected database " + database["label"] + " is not currently available.")


# ======= Callbacks for modal popup =======
@app.callback(
    Output("markdown", "style"),
    [Input("learn-more-button", "n_clicks"),
     Input("markdown_close", "n_clicks")],
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
    app.run_server(port=8050, debug=True, dev_tools_ui=True,
                   dev_tools_props_check=True)
