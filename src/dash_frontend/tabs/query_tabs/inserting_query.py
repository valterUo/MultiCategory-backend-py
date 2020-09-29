import dash_core_components as dcc
import dash_html_components as html
from dash_frontend.state.initialize_demo_state import state
from dash_frontend.server import app
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from dash_frontend.tabs.query_tabs.insert_query_elements.build_insert_tool import build_insert_tool
fold_query_state = []


def insert_query_subtab():
    return dcc.Tab(
        id="Insert-query-subtab",
        label="Insert queries",
        value="subtab4",
        className="custom-tab",
        selected_className="custom-tab--selected",
    )


def build_insert_query_subtab():
    objects = state.get_current_state()["db"].get_objects()
    options = []
    for obj in objects:
        options.append({'label': str(obj), 'value': str(obj)})

    return [html.Div(id="insert-query-subtab-main-container", children=[
        html.Div(
            id="set-specs-intro-container",
            children=[
        html.Label([
            "Select collection to insert",
            dcc.Dropdown(
                id="select-insert-dataset",
                style={'width': '90%',
                                "display": "block"},
                options=options
            )]),
            html.Div(id = "insert-tool")
    ])])]

@app.callback(
    Output("insert-tool", "children"),
    [Input("select-insert-dataset", "value")],
)
def update_click_output(dataset):
    if dataset != "" and dataset != None:
        objects = state.get_current_state()["db"].get_objects()
        return build_insert_tool(objects[dataset])
    else:
        raise PreventUpdate