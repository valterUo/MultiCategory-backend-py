import dash
import dash_table
import pandas as pd

## df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')
## https://plotly.com/python/v3/ipython-notebooks/pytables/

def pytables_visualization(table):
    df = None
    return dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
    )