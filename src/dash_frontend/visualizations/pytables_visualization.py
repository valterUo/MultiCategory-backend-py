import dash
import dash_table
import pandas as pd
from IPython.display import display
import chart_studio.plotly as py # interactive graphing
from plotly.graph_objs import Bar, Scatter, Marker, Layout, Data, Figure, Heatmap, XAxis, YAxis
import plotly.tools as tls
import numpy as np
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
from dash_frontend.state.initialize_demo_state import multi_model_join_results
from dash_frontend.server import app
from dash.dependencies import Input, Output
amount_of_rows = 50

def main_pytable_visualization():
    table = multi_model_join_results.get_current_state()
    return html.Div(id = "pytables-visualization", children = [
        dcc.Graph(id = "pytable-figure", style = {'height': '1000px'}, config= {}, figure = pytables_visualization(table, amount_of_rows)),
        html.P("Number of rows shown max: " + str(amount_of_rows)),
        html.Button(id='fetch-more-button', n_clicks=0,
                                children='Show more')
        ])

def pytables_visualization(table, amount_of_rows):
    table_data = []
    print(table)
    print(table.get_collection())
    pytable = table.get_collection().get_iterable_collection_of_objects()

    for name in pytable.colnames:
        values = pytable.cols._f_col(name)[:amount_of_rows]
        binary_values = values.tolist()
        decoded_values = []
        for value in binary_values:
            try:
                decoded_values.append(value.decode('utf-8'))
            except:
                decoded_values.append(value)
        table_data.append(decoded_values)

    fig = go.Figure(layout = {
                'title': table.get_name() + " visualization"
            }, data=[go.Table(
        header=dict(values=pytable.colnames,
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values= table_data,
                fill_color='lavender',
                align='left'))
    ])

    return fig

@app.callback(
    Output('"pytable-figure"', 'figure'),
    [Input('fetch-more-button', 'n_clicks')])
def fetch_more(n_clicks):
    global amount_of_rows
    amount_of_rows = amount_of_rows + 50
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "fetch-more-button":
            table = multi_model_join_results.get_current_state()
            return pytables_visualization(table, amount_of_rows)
    else:
        raise PreventUpdate