import dash
import dash_core_components as dcc
import dash_html_components as html
import os
import glob
from dash_frontend.server import app
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from external_database_connections.postgresql.postgres import Postgres
from model_transformations.query_language_transformations.SQL.sql import SQL
from external_database_connections.config.config import config
dirname = os.path.dirname(__file__)
example_files_path = os.path.join(dirname, "..\\..\\model_transformations\\ldbc\\ldbc_sql\\*.sql")


def query_tranformation_tab():
    return dcc.Tab(
        id="Query-transformation-tab",
        label="Query Transformations",
        value="subtab3",
        className="custom-tab",
        selected_className="custom-tab--selected",
    )


def build_query_tranformation_tab():
    sql_examples = parse_sql_query_examples()
    cypher_examples = []
    rel_params = config(section= "postgresql")
    return [
        html.Div(
            id="set-specs-intro-container",
            children=[html.H5("SQL to Cypher query transformation"), 
            html.Div(style={"width": "100%", "display": "inline-block"}, children = [ html.Div(id="connected_external_database", children = [
                html.P("You are connected to PostgreSQL database " + rel_params["database"] + ".")]),
                      html.Div(id="sql-container", style={"width": "49%", "display": "inline-block"}, children=[
                          html.H5(
                               "SQL"
                               ),
                          dcc.Dropdown(
                              id="sql-to-cypher-query-transformation",
                              options=sql_examples,
                              style={'width': '90%'}
                          ), dcc.Textarea(
                                  id="sql-query-input",
                                  value="",
                                  style={'width': '90%', 'height': 600, "fontFamily": "monospace"},
                              ),
                          html.Button(id="transform-sql-query", children="TRANSFORM"), ]),
                      html.Div(id="cypher-container", style={"width": "49%", "display": "inline-block"}, children=[
                          html.H5("Cypher"),
                          dcc.Dropdown(
                              id="cypher-to-sql-query-transformation",
                              options=cypher_examples,
                              style={'width': '90%'}
                          ),
                              dcc.Textarea(
                                  id="cypher-query-input",
                                  value="",
                                  style={'width': '90%', 'height': 600, "fontFamily": "monospace"},
                              ),
                      html.Button(id="transform-cypher-query", children="TRANSFORM"),]) ])
                      ])
    ]


@app.callback(
    Output("sql-query-input", "value"),
    [Input("sql-to-cypher-query-transformation", "value")]
)
def update_selected_query_example(query):
    if query != None:
        return query
    else:
        return ""


@app.callback(
    Output("cypher-query-input", "value"),
    [Input("transform-sql-query", "n_clicks")],
    [State("sql-query-input", "value")]
)
def execute_query_transformation(button_click, query):
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "transform-sql-query":
            db = Postgres("ldbcsf1")
            elem = SQL("test", query, db)
            result = elem.get_cypher()
            return result
    else:
        raise PreventUpdate


def parse_sql_query_examples():
    examples = []
    example_filenames = glob.glob(example_files_path)
    for i, file_name in enumerate(example_filenames):
        with open(file_name, 'r') as reader:
            lines = reader.read()
            examples.append({'label': 'example ' + os.path.basename(file_name), 'value': lines})
    return examples
