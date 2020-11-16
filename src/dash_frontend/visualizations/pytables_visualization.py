import dash
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
from dash_frontend.server import app
from dash.dependencies import Input, Output
whole_table = None
amount_of_rows = 50


def main_pytable_visualization(visualized_object):
    global whole_table
    whole_table = visualized_object
    fig = pytables_visualization(visualized_object, amount_of_rows)
    return html.Div(id="pytables-visualization", children=[
        dcc.Graph(id="pytable-figure",
                  style={'height': '1000px'}, config={}, figure=fig),
        html.P("Number of rows shown initially: " + str(amount_of_rows)),
        html.Button(id='fetch-more-button', children='SHOW MORE ROWS')])


def pytables_visualization(table, amount_of_rows):
    table_data = []
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

    fig = go.Figure(layout={
        'title': table.get_name() + " visualization"
    }, data=[go.Table(
        header=dict(values=pytable.colnames,
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=table_data,
                   fill_color='lavender',
                   align='left'))
             ])
    return fig


@app.callback(
    Output('pytable-figure', 'figure'),
    [Input('fetch-more-button', 'n_clicks')])
def fetch_more(n_clicks):
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "fetch-more-button":
            global amount_of_rows
            amount_of_rows += 50
            return pytables_visualization(whole_table, amount_of_rows)
    else:
        raise PreventUpdate
