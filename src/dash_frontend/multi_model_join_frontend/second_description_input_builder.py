import dash
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
from tables import *
from dash_frontend.server import app
from dash.dependencies import Input, Output

def second_description_input_builder(state_dict, domain, target):
    # description = dict()
    # description["customer_id"] = StringCol(64, dflt='NULL')
    # description["name"] = StringCol(64, dflt='NULL')
    # description["creditLimit"] = StringCol(64, dflt='NULL')
    # description["customer_locationId"] = StringCol(64, dflt='NULL')

    html.Div([
        html.Div(id="second_description_inputs", children=[
            dcc.Input(
                id="input_description",
                placeholder="add attribute",
                type="text"
            ),
            html.Button(id='add_description_input', type="primary",
                        n_clicks=0, children='Add attribute'),
            html.Div(id = "added_descriptions")
        ]
        ),
        html.Div([
            html.Button(id='submit_description_input', type="primary",
                        n_clicks=0, children='Submit attributes')
        ]),
    ]
    )


@app.callback(
    output=Output("added_descriptions", "children"),
    inputs=[Input("input_description", "value"),
            Input("add_description_input", "n_clicks")]
)
def add_input(children, value, n_clicks):
    ctx = dash.callback_context
    prop_id = ""
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if prop_id == "add_description_input":
            return html.P(value)


@app.callback(
    output=Output("second_description_inputs", "children"),
    inputs=[Input("submit_description_input", "n_clicks")]
)
def submit_input(children):
    ctx = dash.callback_context
    prop_id = ""
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if prop_id == "submit_description_input":
            button = children.pop()
