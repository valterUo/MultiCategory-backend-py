import dash_core_components as dcc
import dash_html_components as html
from dash_frontend.tabs.model_transformation_tabs.data_transformation_tab import data_tranformation_tab, build_data_tranformation_tab
from dash_frontend.tabs.model_transformation_tabs.query_transformation_tab import query_tranformation_tab, build_query_tranformation_tab
from dash_frontend.server import app
from dash.dependencies import Input, Output


def transformation_tabs():
    return dcc.Tab(
        id="Transformation-tab",
        label="Transformations",
        value="tab5",
        className="custom-tab",
        selected_className="custom-tab--selected",
    )


def build_transformation_tabs():
    return [html.Div([
        html.Div(
            id="subtabs",
            className="tabs",
            children=[
                dcc.Tabs(
                    id="app-subtabs",
                    value="subtab4",
                    className="custom-tabs",
                    children=[
                        data_tranformation_tab(),
                        query_tranformation_tab()
                    ],
                ),
            ],
        ),
        html.Div(id="transformation-subtab-container")
    ])]

# ======= Callbacks for changing subtabs =======


@app.callback(
    Output("transformation-subtab-container", "children"),
    [Input("app-subtabs", "value")],
)
def render_tab_content(tab_switch):
    if tab_switch == "subtab3":
        return build_query_tranformation_tab()
    elif tab_switch == "subtab4":
        return build_data_tranformation_tab()
