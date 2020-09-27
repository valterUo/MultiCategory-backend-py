import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash_frontend.state.initialize_demo_state import state
from dash_frontend.server import app
from category_of_collection_constructor_functors.collections.tree_collection import TreeCollection
from category_of_collection_constructor_functors.model_categories.category_of_tree_model import TreeModelCategory
from category_of_collection_constructor_functors.collection_constructor import CollectionConstructor
import os
dirname = os.path.dirname(__file__)
name = ""

def build_tree_constructor():
    return [html.Div(id = "build-relational-constructor-main", children=[
         html.Label([
            "Give a name for this object", html.Br(),
            dcc.Input(
                id="tree-constructor-name-input",
                type="text",
                value="",
                placeholder="name",
                style={'width': '90%', "display": "inline-block"},
            )]), 
            html.Button(id = "submit-tree-constructor"),
            html.Div(id = "tree-constructor-notification")
    ])]

@app.callback(
    [Output("tree-constructor-notification", "children")]
    [Input("submit-tree-constructor", "n_clicks")]
    [State("tree-constructor-name-input", "value")],
)
def name_input(n_clicks, name):
    target_folder_path = os.path.join(dirname, "..\\..\\db_files")
    model_category = TreeModelCategory(name)
    collection = TreeCollection(name, target_file_path=target_folder_path)
    constructor = CollectionConstructor(name, model_category, collection)
    state.get_current_state()["db"].add_object(constructor)
    return html.P("New tree collection constructor added to the multi-model database.")