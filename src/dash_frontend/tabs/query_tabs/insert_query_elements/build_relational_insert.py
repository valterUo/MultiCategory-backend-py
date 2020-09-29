import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash_frontend.state.initialize_demo_state import state
from dash_frontend.server import app
from dash.dependencies import Input, Output, State, MATCH
from dash.exceptions import PreventUpdate
constructor = None
inserted_rows = []
current_row = dict()

def build_relational_insert(root, collection_constructor):
    global constructor
    constructor = collection_constructor
    attributes_datatypes = collection_constructor.get_collection().get_attributes_datatypes_dict()
    attributes = list(attributes_datatypes.keys())
    column_inputs = [
        html.Div(id={
                'type': 'dynamic-input',
                'index': "{}".format(_)
            }, children = [dcc.Input(
            id = "column-input-field_{}".format(_),
            type="text",
            style = {"width": "51%"},
            placeholder="input " + "{}".format(_) + " in type " + str(attributes_datatypes[_]),
            value = ""
        ), html.Div(id= "attribute-info_{}".format(_), style = {"display": "none"}, children = [_])])
        for _ in attributes
    ]

    return html.Div(id = "tree-insert-main-container", children = [
    html.Div(id = "column_inputs", children =
        [html.H6("Input columns for table " + collection_constructor.get_name())] +
        column_inputs +
        [html.Br(), html.Button(id = "submit-row", children = "INSERT ROW IN TABLE"), html.Div(id = "hidden-attribute-element", style = {"display": "none"}, children = attributes)]
    ),
    html.Br(),
    html.Div(id = "value-summary", style = {"visibility": "hidden"}, children = [
    html.H6("Following values will be inserted:"),
    html.Div(children = [html.Div(id = {'type': 'inserted-rows', 'index': "{}".format(_)}) for _ in attributes])]),
    html.Br(),
    html.Button(id = "commit-rows-into-table", children = "COMMIT ROWS TO TABLE"),
    html.Div(id = "final-success-nofication")
    ])

# @app.callback(
#     [Output("inserted-rows", "children")], #+ [Output("input_{}".format(_), "value") for _ in attributes],
#     [Input("submit-row", "n_clicks"), Input("hidden-attribute-element", "children")],
# )
# def cb_render(n_clicks, attributes):
#     ctx = dash.callback_context
#     if ctx.triggered:
#         prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
#         if prop_id == "submit-row":
#             columns = [{"name": i, "id": i} for i in attributes]
#             data = dict()
#             #for i in range(len(attributes)):
#             #    data[attributes[i]] = vals[i]
#             #global inserted_rows
#             #inserted_rows.append(data)
#             #print(vals)
#             return [str(attributes)] #[dash_table.DataTable(
#             #         id='inserted-data-table',
#             #         columns=columns,
#             #         data=inserted_rows,
#             #     )] + ["" for i in range(len(vals))]
#         else:
#             raise PreventUpdate
#     else:
#         raise PreventUpdate

@app.callback(
    Output({'type': 'inserted-rows', 'index': MATCH}, 'children'),
    [Input("submit-row", "n_clicks")],
    [State({'type': 'dynamic-input', 'index': MATCH}, 'children')], prevent_initial_call=True
)
def handle_row_input(n_clicks, value):
    data = value[0]["props"]["value"]
    attribute = value[1]["props"]["children"][0]
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "submit-row":
            global current_row
            current_row[attribute] = data
            return html.P(attribute + " : " + data)
    else:
        raise PreventUpdate

@app.callback(
    Output("value-summary", "style"), 
    [Input("submit-row", "n_clicks")],
)
def cb_render(n_clicks):
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "submit-row":
            global inserted_rows
            inserted_rows.append(current_row)
            return {"visibility": "visible"}
    else:
        raise PreventUpdate

@app.callback(
    Output("final-success-nofication", "children"), 
    [Input("commit-rows-into-table", "n_clicks")],
)
def cb_render(n_clicks):
    global inserted_rows
    row_n = len(inserted_rows)
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "commit-rows-into-table":
            constructor.append_to_collection(inserted_rows)
            return html.P(str(row_n) + " were inserted into " + constructor.get_name() + " succesfully.")
    else:
        raise PreventUpdate
