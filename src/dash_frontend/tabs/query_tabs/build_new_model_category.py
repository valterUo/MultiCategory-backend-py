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
from dash_frontend.tabs.query_tabs.building_constructors.build_graph_constructor import build_graph_constructor
from dash_frontend.tabs.query_tabs.building_constructors.build_relational_constructor import build_relational_constructor
from dash_frontend.tabs.query_tabs.building_constructors.build_tree_constructor import build_tree_constructor

def build_new_model_category():
    return html.Div(id = "build-new-model-category-main-container", style = {"display": "block"}, children = [
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
                    html.Button(id = "add-selected-model-category", children = "ADD MODEL CATEGORY"), html.Br(),
                    html.Div(id = "collection-definition-container", style = {"margin": "5px", "border": "1px solid white", "padding": "10px"}, children = [
                        html.Div(id = "collection-definition")
                        ]), html.Br(),
                    html.Div(id = "current-model-category")
        ])
    ])

@app.callback(
    [Output("current-model-category", "children"), 
    Output("collection-definition", "children")],
    [Input("add-selected-model-category", "n_clicks")],
    [State("select-model-category-for-new-model", "value"), 
    State("collection-definition", "children")]
)
def update_click_output(n_clicks, value, current_children):
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
            if current_children == None:
                current_children = []
            if value == "relational":
                current_children.append(build_relational_constructor())
            elif value == "graph":
                current_children.append(build_graph_constructor())
            elif value == "tree":
                current_children.append(build_tree_constructor())
            current_children.append(html.Hr())
            return model_category_building_tool(model_category), current_children
    raise PreventUpdate