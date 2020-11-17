import dash
import dash_core_components as dcc
import dash_html_components as html
from tables import *
from dash_frontend.server import app
from dash.dependencies import Input, Output, State
from dash_frontend.state.parameter_state import parameter_state
from dash_frontend.state.automatic_table_settings import automatic_example_settings_dict
from dash.exceptions import PreventUpdate
attributes = dict()


def second_description_input_builder():
    return html.Div([
        html.Div(id="second_description_inputs", children=[html.Div(style={'width': '100%', 'display': 'inline-block', 'position': 'relative'}, children=[
            dcc.Input(
                id="input_description",
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
            html.Button(id='add_description_input', style={
                        "margin": "5px"}, children='Add attribute'),
            html.Div(id="added_descriptions", children=[]),
            html.Div(id="second_description_input_notification"),
            html.Div(id="automatic-example-added_descriptions", children=[]),
            html.Div(id="automatic-example-second_description_input_notification")
        ]
        ),
        html.Div([
            html.Br(),
            html.Button(id='submit_description_input',
                        children='Submit attributes'),
            html.Button(id='apply-automatic-example-settings', children='Apply automatic example settings',
                        style={'display': "inline-block", "margin": "10px"})
        ]),
    ]
    )


@app.callback(
    output=[Output("added_descriptions", "children"),
            Output("input_description", "value")],
    inputs=[Input("add_description_input", "n_clicks")],
    state=[State("input_description", "value"), State(
        "pytable-datatype-dropdown", "value"), State("added_descriptions", "children")]
)
def add_input(n_clicks, value, datatype, current_children):
    global attributes
    datatypes = {"StringCol(64, dflt='NULL')": StringCol(64, dflt='NULL'), "Int64Col(dflt = 0)": Int64Col(
        dflt=0), "Float32Col(dflt = 0)": Float32Col(dflt=0)}
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
            return current_children, ""
    return current_children, ""


@app.callback(
    output=[Output("second_description_input_notification", "children"),
            Output("input_description", "disabled")],
    inputs=[Input("submit_description_input", "n_clicks"),
            Input("added_descriptions", "children")]
)
def submit_input(n_clicks, children):
    global attributes
    ctx = dash.callback_context
    prop_id = ""
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "submit_description_input":
            global parameter_state
            parameter_state["second_description"] = attributes
            return html.P("Attributes added! The attributes input field is closed now."), True
    return [], False


@app.callback(
    [Output("automatic-example-added_descriptions", "children"),
     Output("automatic-example-second_description_input_notification", "children"),
     Output('add_description_input', "disabled")],
    [Input("apply-automatic-example-settings", "n_clicks")]
)
def submit_input(n_clicks):
    ctx = dash.callback_context
    prop_id = ""
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        content = []
        if prop_id == "apply-automatic-example-settings":
            global parameter_state
            domain = parameter_state["domain"]
            target = parameter_state["target"]
            parameter_state["second_description"] = automatic_example_settings_dict[domain][target]
            description = parameter_state["second_description"]
            for elem in description:
                content.append(html.P("Attribute: " + elem +
                                      ". Datatype in table: " + str(description[elem])))
        return content, html.P("Attributes added! The attributes adding tool is closed now."), True
    else:
        raise PreventUpdate
