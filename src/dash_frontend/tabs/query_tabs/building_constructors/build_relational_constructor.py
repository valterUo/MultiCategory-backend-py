import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash_frontend.state.initialize_demo_state import state
from dash_frontend.server import app
from dash_frontend.tabs.query_tabs.input_attributes_for_table import attributes_for_table_input_builder
from category_of_collection_constructor_functors.collections.table_collection import TableCollection
from category_of_collection_constructor_functors.model_categories.category_of_table_model import TableModelCategory
from category_of_collection_constructor_functors.collection_constructor import CollectionConstructor
import os
dirname = os.path.dirname(__file__)
name = ""

def build_relational_constructor():
    return [html.Div(id = "build-relational-constructor-main", children=[
         html.Label([
            "Give a name for this object", html.Br(),
            dcc.Input(
                id="relational-constructor-name-input",
                type="text",
                value="",
                placeholder="name",
                style={'width': '90%', "display": "inline-block"},
            )]), html.Br(),
        attributes_for_table_input_builder()
    ])]

@app.callback(
    [Input("relational-constructor-name-input", "value")],
)
def name_input(value):
    global name
    name = value


def return_attibutes_to_build_relational_constructor(attributes_datatypes):
    target_folder_path = os.path.join(dirname, "..\\..\\db_files")
    model_category = TableModelCategory(name, list(attributes_datatypes.keys()))
    collection = TableCollection(name, attributes_datatypes, h5file_path = target_folder_path + "\\" + name + ".h5")
    constructor = CollectionConstructor(name, model_category, collection)
    state.get_current_state()["db"].add_object(constructor)