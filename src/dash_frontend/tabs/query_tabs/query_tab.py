import dash_core_components as dcc
import dash_html_components as html
from dash_frontend.tabs.query_tabs.selective_query_subtab import selective_query_subtab, build_selective_query_subtab
from dash_frontend.tabs.query_tabs.create_morphism_subtab import create_morphism_subtab, build_create_morphism_subtab
from dash_frontend.tabs.query_tabs.create_object_subtab import create_object_subtab, build_create_object_subtab
from dash_frontend.server import app
from dash.dependencies import Input, Output


def query_tabs():
    return dcc.Tab(
        id="Query-tab",
        label="Queries",
        value="tab3",
        className="custom-tab",
        selected_className="custom-tab--selected",
    )


def build_query_tabs():
    return [html.Div([
        html.Div(
            id="subtabs",
            className="tabs",
            children=[
                dcc.Tabs(
                    id="app-subtabs",
                    value="subtab1",
                    className="custom-tabs",
                    children=[
                        selective_query_subtab(),
                        create_morphism_subtab(),
                        create_object_subtab()
                    ],
                ),
            ],
        ),
        html.Div(id="query-subtab-container")
    ])]

# ======= Callbacks for changing subtabs =======


@app.callback(
    Output("query-subtab-container", "children"),
    [Input("app-subtabs", "value")],
)
def render_tab_content(tab_switch):
    if tab_switch == "subtab1":
        return build_selective_query_subtab()
    elif tab_switch == "subtab2":
        return build_create_morphism_subtab()
    elif tab_switch == "subtab3":
        return build_create_object_subtab()
    return build_selective_query_subtab()
