import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash_frontend.state.initialize_demo_state import state
from dash_frontend.server import app
from category_of_collection_constructor_functors.collections.table_collection import TableCollection
from category_of_collection_constructor_functors.model_categories.category_of_table_model import TableModelCategory
from category_of_collection_constructor_functors.collection_constructor import CollectionConstructor
import os
from tables import *
attributes = dict()
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
            )]), html.Button(id = "submit-relational-object-name", children = "SUBMIT NAME"), html.Div(id = "name-notification"), html.Br(),
        attributes_for_table_input_builder()
    ])]

@app.callback( Output("name-notification", "children"), 
[Input("submit-relational-object-name", "n_clicks")], 
[State("relational-constructor-name-input", "value")]
)
def name_input(n_clicks, value):
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "submit-relational-object-name" and value.strip() != "":
            global name
            name = value
            return html.P("Name " + name + " submitted.")
        else:
            raise PreventUpdate
    else:
            raise PreventUpdate


def attributes_for_table_input_builder():
    return html.Div([
        html.Div(id="attributes_for_table_input_container", children=[
            html.Div(style={'width': '100%', 'display': 'block', 'position': 'relative'}, children=[
            dcc.Input(
                id="attributes_for_table_input",
                placeholder="Add attribute",
                type="text",
                style={'width': '49%', 'display': 'inline-block'}
            ),
            dcc.Dropdown(
                id="pytable-datatype-dropdown",
                style={'width': '49%', 'display': 'inline-block',
                       "marginLeft": "10px", 'bottom': "0px", 'left': "0px"},
                options=[{'label': 'String', 'value': "StringCol(64, dflt='NULL')"}, {
                    'label': 'Int', 'value': "Int64Col(dflt = 0)"}, {'label': 'Float', 'value': "Float32Col(dflt = 0)"}],
                value="StringCol(64, dflt='NULL')",
            )]),
            html.Button(id='add_attributes_for_table_input', type="primary", style={"margin": "5px"},
                        n_clicks=0, children='ADD ATTRIBUTE'),
            html.Div(id="added_attributes", children=[]),
            html.Div(id="attributes_for_table_input_notification")]
        ),
        html.Div([
            html.Br(),
            html.Button(id='submit_attributes_for_table_input', type="primary",
                        n_clicks=0, children='Submit attributes')
        ]),
    ]
    )


@app.callback(
    [Output("added_attributes", "children"),
    Output("attributes_for_table_input", "value")],
    [Input("add_attributes_for_table_input", "n_clicks")],
    [State("attributes_for_table_input", "value"), 
    State("pytable-datatype-dropdown", "value"), 
    State("added_attributes", "children")]
)
def add_input(n_clicks, value, datatype, current_children):
    global attributes
    datatypes = {"StringCol(64, dflt='NULL')": StringCol(64, dflt='NULL'), "Int64Col(dflt = 0)": Int64Col(dflt=0), "Float32Col(dflt = 0)": Float32Col(dflt=0)}
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "add_attributes_for_table_input" and value.strip() != "":
            attributes[value.strip()] = datatypes[datatype]
            if current_children == None:
                return [html.P("Attribute: " + value + ". Datatype: " + str(datatype))], ""
            current_children.append(
                html.P("Attribute: " + value + ". Datatype in table: " + datatype))
            return current_children, ""
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

@app.callback(
    [Output("attributes_for_table_input_notification", "children"),
    Output("attributes_for_table_input", "disabled")],
    [Input("submit_attributes_for_table_input", "n_clicks")]
)
def submit_input(n_clicks):
    global attributes
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "submit_attributes_for_table_input":
           return_attibutes_to_build_relational_constructor(attributes)
           return html.P("New relational collection with name '" + name + "' has been added to the multi-model database."), True
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

def return_attibutes_to_build_relational_constructor(attributes_datatypes):
    target_folder_path = os.path.join(dirname, "..\\..\\db_files")
    model_category = TableModelCategory(name, list(attributes_datatypes.keys()))
    collection = TableCollection(name, attributes_datatypes, h5file_path = target_folder_path + "\\" + name + ".h5")
    constructor = CollectionConstructor(name, model_category, collection)
    state.get_current_state()["db"].add_object(constructor)