import dash
import dash_core_components as dcc
import dash_html_components as html
from tables import *
from dash_frontend.server import app
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash_frontend.tabs.query_tabs.building_constructors.build_relational_constructor import return_attibutes_to_build_relational_constructor
attributes = dict()

def attributes_for_table_input_builder():
    return html.Div([
        html.Div(id="attributes_for_table_input_container", children=[
            html.Div(style={'width': '100%', 'display': 'none', 'position': 'relative'}, children=[
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
            html.Button(id='add_description_input', type="primary", style={"margin": "5px"},
                        n_clicks=0, children='Add attribute'),
            html.Div(id="add_attributes", children=[]),
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
    [Output("added_descriptions", "children"),
    Output("input_description", "value")],
    [Input("add_description_input", "n_clicks")],
    [State("input_description", "value"), 
    State("pytable-datatype-dropdown", "value"), 
    State("added_descriptions", "children")]
)
def add_input(n_clicks, value, datatype, current_children):
    global attributes
    datatypes = {"StringCol(64, dflt='NULL')": StringCol(64, dflt='NULL'), "Int64Col(dflt = 0)": Int64Col(dflt=0), "Float32Col(dflt = 0)": Float32Col(dflt=0)}
    ctx = dash.callback_context
    prop_id = ""
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "add_description_input" and value.strip() != "":
            attributes[value.strip()] = datatypes[datatype]
            if current_children == None:
                return [html.P("Attribute: " + value + ". Datatype: " + str(datatype))], ""
            current_children.append(
                html.P("Attribute: " + value + ". Datatype in table: " + datatype))
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

@app.callback(
    [Output("attributes_for_table_input_notification", "children"),
    Output("attributes_for_table_input", "disabled")],
    [Input("submit_attributes_for_table_input", "n_clicks"),
    Input("add_attributes", "children")]
)
def submit_input(n_clicks, children):
    global attributes
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "submit_description_input":
           return_attibutes_to_build_relational_constructor(attributes)
           return html.P("Attributes added! The attributes input field is closed now."), True
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
