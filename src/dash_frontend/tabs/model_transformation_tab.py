import dash
import dash_core_components as dcc
import dash_html_components as html
import os
from dash_frontend.server import app
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from model_transformations.query_language_transformations.SQL.sql import SQL
dirname = os.path.dirname(__file__)
example_file_path = os.path.join(
    dirname, "..\\..\\model_transformations\\ldbc\\bi-10.sql")


def model_tranformation_tab():
    return dcc.Tab(
        id="Model-transformation-tab",
        label="Model Transformations",
        value="tab5",
        className="custom-tab",
        selected_className="custom-tab--selected",
    )


def build_model_tranformation_tab():
    sql_examples = parse_sql_query_examples()
    cypher_examples = []
    return [
        html.Div(
            id="set-specs-intro-container",
            children=[html.H5("SQL to Cypher query transformation"), html.Div(style={"width": "100%", "display": "inline-block"}, children = [
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
            primary_foreign_keys = ["p_personid", "pt_personid", "pt_tagid", "t_tagid", "m_creatorid",
                                    "m_messageid", "mt_messageid", "mt_tagid", "k_person1id", "personid", "k_person2id"]
            elem = SQL("test", query, primary_foreign_keys)
            result = elem.get_cypher(elem)
            return result
    else:
        raise PreventUpdate


def parse_sql_query_examples():
    examples = []
    with open(example_file_path, 'r') as reader:
        lines = reader.read()
        examples.append({'label': 'example 1', 'value': lines})
    return examples
