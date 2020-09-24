import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash_frontend.server import app
from dash.exceptions import PreventUpdate
from dash_frontend.visualizations.model_category_building_tool import model_category_building_tool
from category_of_collection_constructor_functors.model_categories.category_of_graph_model import GraphModelCategory
from category_of_collection_constructor_functors.model_categories.category_of_table_model import TableModelCategory
from category_of_collection_constructor_functors.model_categories.category_of_tree_model import TreeModelCategory

def build_new_model_category():
    return html.Div(id = "build-new-model-category-main-container", style = {"display": "none"}, children = [
        html.Div(id = "select-added-model-category", children = [
            html.Label([
                    "Select model category",
                    dcc.Dropdown(
                        id="select-model-category-for-new-model",
                        style={'width': '49%',
                                        "display": "block"},
                        options=[{'label': 'relational', 'value': 'relational'},
                                    {'label': 'property graph',
                                            'value': 'graph'},
                                    {'label': 'tree',
                                            'value': 'tree'}]
                    )]),
                    html.Br(),
                    html.Button(id = "add-selected-model-category", children = "ADD MODEL CATEGORY"),
                    html.Div(id = "current-model-category")
        ])
    ])

@app.callback(
    Output("current-model-category", "children"),
    [Input("add-selected-model-category", "n_clicks")],
    [State("select-model-category-for-new-model", "value")]
)
def update_click_output(n_clicks, value):
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "add-selected-model-category" and value != None:
            model_category = None
            if value == "relational":
                model_category = TableModelCategory("test_table")
            elif value == "graph":
                model_category = GraphModelCategory("test_graph")
            elif value == "tree":
                model_category = TreeModelCategory("test_tree")
            return model_category_building_tool(model_category)
    raise PreventUpdate