import dash
import dash_core_components as dcc
import dash_html_components as html
import os
import glob

from dash_html_components import Pre
from dash_frontend.server import app
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash_frontend.tabs.model_transformation_tabs.construct_postgres_schema import construct_postgres_schema
from external_database_connections.neo4j.neo4j import Neo4j
from external_database_connections.postgresql.postgres import Postgres
from model_transformations.query_language_transformations.SQL.sql import SQL
from external_database_connections.config.config import config
dirname = os.path.dirname(__file__)
example_files_path = os.path.join(
    dirname, "..\\..\\model_transformations\\ldbc\\ldbc_sql\\*.sql")

rel_db = Postgres("lcdbsf1")
graph_db = Neo4j("lcdbsf1")


def data_tranformation_tab():
    return dcc.Tab(
        id="Data-transformation-tab",
        label="Data Transformations",
        value="subtab4",
        className="custom-tab",
        selected_className="custom-tab--selected",
    )


def build_data_tranformation_tab():    
    return [
        html.Div(
            id="set-specs-intro-container",
            children=[html.H5("PostgreSQL to Neo4j data transformation"),
                      html.Div(id="data-transformation-notifications", children = [notify_db_not_empty()]),
                      html.Button("LOAD SCHEMA FROM POSTGRESQL", id = "load-schema-postgres"),
                      html.Div(id = "postgres-schema-container")
                      ]
        )
    ]

def notify_db_not_empty():
    if not graph_db.is_empty():
        return html.Div(id = "proceed-with-nonempty-db", style={"margin": "10px", "border": "1px solid white"}, children = [
            html.P("The graph database is not empty. How do you want to proceed?"),
            html.Button("Empty the graph database", id = "empty-graph-db"),
            html.Button("Append to the graph database", id = "append-graph-db")])
    else:
        return html.Div(html.P("The graph database " + graph_db.get_name() + " is empty."))

@app.callback(
    [Output("proceed-with-nonempty-db", "style"), 
    Output("data-transformation-notifications", "children")],
    [Input("empty-graph-db", "n_clicks"), 
    Input("append-graph-db", "n_clicks")],
)
def handle_not_empty_database_button(click1, click2):
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "empty-graph-db":
            graph_db.empty_database()
            return {}, html.Div(html.P("The graph database " + graph_db.get_name() + " is empty."))
        elif prop_id == "append-graph-db":
            return {"display": "none"}, [] 
    else:
        raise PreventUpdate

@app.callback(
    Output("postgres-schema-container", "children"),
    [Input("load-schema-postgres", "n_clicks")],
)
def handle_not_empty_database_button(click1):
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "load-schema-postgres":
            return construct_postgres_schema(rel_db)
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate