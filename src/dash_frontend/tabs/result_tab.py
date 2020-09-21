import dash
import dash_core_components as dcc
import dash_html_components as html
from dash_frontend.server import app
from dash.dependencies import Input, Output, State
from dash_frontend.state.initialize_demo_state import state
from dash.exceptions import PreventUpdate
from dash_frontend.server import app
from dash_frontend.visualizations.visualize import visualize


def result_tab():
    return dcc.Tab(
        id="Result-tab",
        label="Result",
        value="tab6",
        className="custom-tab",
        selected_className="custom-tab--selected",
    )


def build_result_tab():
    objects = state.get_current_state()["db"].get_objects()
    initial_options = []
    for obj in objects:
        initial_options.append({'label': str(obj), 'value': str(obj)})

    return [html.Div(
            id="set-specs-intro-container", children = [
                html.Div(id="result-tab-main-container", children=[
        html.Div(id="select-visualized-object", children=[
            html.H4(
                "This area is for creating selective queries and creating new objects and morphisms to the selected multi-model database."
            ),
            html.Hr(),
            html.Label(children=[
                html.H6(
                    "Visualize the selected object (includes results to queries): "),
                dcc.Dropdown(
                    id="select-visualized-object-dropdown",
                    style={'width': '50%'},
                    options=initial_options,
                )]),
            html.Button(id="show-result-button", children="VISUALIZE"),
            html.Hr(),
            html.Div(id="main-result-container")
        ])
    ])]
    )]


@app.callback(
    Output("main-result-container", "children"),
    [Input("show-result-button", "n_clicks")],
    [State("select-visualized-object-dropdown", "value")]
)
def update_click_output(button_click, selected_dataset):
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "show-result-button":
            return html.Div(visualize(selected_dataset))
    else:
        raise PreventUpdate
