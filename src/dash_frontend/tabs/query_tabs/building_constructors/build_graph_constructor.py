import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash_frontend.state.initialize_demo_state import state
from dash_frontend.server import app
from category_of_collection_constructor_functors.collections.graph_collection import GraphCollection
from category_of_collection_constructor_functors.model_categories.category_of_graph_model import GraphModelCategory
from category_of_collection_constructor_functors.collection_constructor import CollectionConstructor
import os
dirname = os.path.dirname(__file__)
name = ""

def build_graph_constructor():
    return [html.Div(id = "build-relational-constructor-main", children=[
         html.Label([
            "Give a name for this object", html.Br(),
            dcc.Input(
                id="graph-constructor-name-input",
                type="text",
                value="",
                placeholder="name",
                style={'width': '90%', "display": "inline-block"},
            )]),
            html.Br(),
            html.Button(id = "submit-graph-constructor", children = "SUBMID GRAPH OBJECT"),
            html.Br(),
            html.Div(id = "graph-constructor-notification")
    ])]

@app.callback(
    [Output("graph-constructor-notification", "children"), 
    Output("graph-constructor-name-input", "value")],
    [Input("submit-graph-constructor", "n_clicks")],
    [State("graph-constructor-name-input", "value")],
)
def name_input(n_clicks, name):
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "submit-graph-constructor" and name.strip() != "":
            target_folder_path = os.path.join(dirname, "..\\..\\db_files")
            model_category = GraphModelCategory(name)
            collection = GraphCollection(name, target_folder_path=target_folder_path)
            constructor = CollectionConstructor(name, model_category, collection)
            state.get_current_state()["db"].add_object(constructor)
            return html.P("New graph collection constructor added to the multi-model database."), ""
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate