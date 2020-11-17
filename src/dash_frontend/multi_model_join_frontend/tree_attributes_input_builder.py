import dash
import dash_core_components as dcc
import dash_html_components as html
from dash_frontend.server import app
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
attributes = []
parameter_state = None


def tree_attributes_input_builder(params):
    global parameter_state
    parameter_state = params
    return html.Div(children=[
        html.P("Input for tree attributes"),
        dcc.Input(
            id="input_for_tree_attributes",
            placeholder="Add attribute",
            type="text",
            style={'width': '30%', "display": "inline-block"}
        ),
        html.Button(id='add_tree_attribute_input', type="primary", style={"margin": "5px", "display": "inline-block"},
                    n_clicks=0, children='Add attribute'),
        html.Div(id="added_tree_attributes", children=[]),
        html.Div(children=[
            html.Button(id='submit_tree_attribute_inputs',
                        type="primary", style={"margin": "5px"},
                        n_clicks=0, children='Submit tree attributes')]
                 ), html.Div(id="tree_attributes_notification")])


@app.callback(
    [Output("added_tree_attributes", "children"),
     Output("input_for_tree_attributes", "value")],
    [Input("add_tree_attribute_input", "n_clicks")],
    [State("input_for_tree_attributes", "value"),
     State("added_tree_attributes", "children")]
)
def add_input(n_clicks, value, current_children):
    global attributes
    ctx = dash.callback_context
    prop_id = ""
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "add_tree_attribute_input" and value.strip() != "":
            attributes.append(value)
            if current_children == None:
                return [html.P("Attribute: " + value)], ""
            current_children.append(html.P("Attribute: " + value))
            return current_children, ""
    else:
        raise PreventUpdate


@app.callback(
    [Output("input_for_tree_attributes", "disabled"), Output(
        "tree_attributes_notification", "children")],
    [Input("submit_tree_attribute_inputs", "n_clicks")]
)
def submit_input(n_clicks):
    global attributes
    ctx = dash.callback_context
    prop_id = ""
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "submit_tree_attribute_inputs":
            parameter_state["tree_attributes"] = attributes
            return True, html.P("Attributes submitted succesfully!")
    else:
        raise PreventUpdate
