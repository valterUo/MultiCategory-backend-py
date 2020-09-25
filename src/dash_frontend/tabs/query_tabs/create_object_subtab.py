import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash_frontend.server import app
from dash_frontend.tabs.query_tabs.build_new_model_category import build_new_model_category

def create_object_subtab():
    return dcc.Tab(
        id="Create-object-subtab",
        label="Create object",
        value="subtab3",
        className="custom-tab",
        selected_className="custom-tab--selected",
    )


def build_create_object_subtab():
    return [html.Div(id = "create_object_subtab-main-container", children = [
        html.Div(
            id="set-specs-intro-container",
            children=[
                html.H4(
                    "This area is for creating new objects into the selected multi-model databases schema and instance categories."
                ),
                html.P("""You can create objects consisting of combinations of implemented data models.
                Objects in the multi-model database are considered to be functors. Thus they consist of a domain category (called model category) and a target category (called collection). 
                The target category is theoretically Set but in the implementation level it is a data structure that follows certain constraints."""),
                html.Hr(),
                html.Label([
                    "Select model category",
                    dcc.Dropdown(
                        id="select-model-category",
                        style={'width': '90%',
                                        "display": "block"},
                        options=[{'label': 'relational', 'value': 'relational'},
                                    {'label': 'property graph',
                                            'value': 'graph'},
                                    {'label': 'tree',
                                            'value': 'tree'},
                                    {'label': 'create new',
                                            'value': 'new'}]
                    )]),
                build_new_model_category(),
            ])
    ])]

@app.callback(
    Output("build-new-model-category-main-container", "style"),
    [Input("select-model-category", "value")],
)
def select_model_category(value):
    if value == "new":
        return {"display": "block"}
    else:
        raise PreventUpdate
