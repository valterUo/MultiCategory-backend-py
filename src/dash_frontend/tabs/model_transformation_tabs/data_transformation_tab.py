import dash
import dash_core_components as dcc
import dash_html_components as html
import os
import glob

from dash_html_components import Pre
from abstract_category.functor.functor import Functor
from abstract_category.functor.functor_error import FunctorError
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

functor = None

tables_to_nodes, tables_to_edges, source_fun, target_fun = [], [], [], []

currently_selected = [{'id': 'forum_tag', 'label': 'forum_tag'},
{'id': 'person_email', 'label': 'person_email'},
{'id': 'person_language', 'label': 'person_language'},
{'id': 'person_tag', 'label': 'person_tag'}] #tables_to_edges


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
                      html.Div(id="data-transformation-notifications",
                               children=[notify_db_not_empty()]),
                      html.Button("LOAD SCHEMA FROM POSTGRESQL",
                                  id="load-schema-postgres"),
                      html.Div(id="postgres-schema-container"),
                      html.Div(id="data-transformation-definition", style={"display": "none"}, children=[
                          html.Div(id="tables_to_edges", style={"width": "24%", "padding": "5px", "display": "inline-block", 'float': 'left', "borderRight": "1px solid white", "borderLeft": "1px solid white", "borderTop": "1px solid white"}, children=[
                              html.H6(
                                  "Select tables that will be mapped to edges"),
                              html.Button("ACTIVATE", id="activate-edges"),
                              html.P("Activated", id="edges-activated")
                          ]),
                          html.Div(id="source-function", style={"width": "25%", "padding": "5px", "display": "inline-block", 'float': 'left', "borderRight": "1px solid white", "borderTop": "1px solid white"}, children=[
                              html.H6(
                                  "Select relationships that will be mapped to source function"),
                              html.Button("ACTIVATE", id="activate-source"),
                              html.P("Not activated", id="source-activated")
                          ]),
                          html.Div(id="target-function", style={"width": "25%", "padding": "5px", "display": "inline-block", 'float': 'left', "borderRight": "1px solid white", "borderTop": "1px solid white"}, children=[
                              html.H6(
                                  "Select relationships that will be mapped to target function"),
                              html.Button("ACTIVATE", id="activate-target"),
                              html.P("Not activated", id="target-activated")
                          ]),
                          html.Div(id="tables_to_nodes", style={"width": "24%", "padding": "5px", "display": "inline-block", 'float': 'left', "borderRight": "1px solid white", "borderTop": "1px solid white"}, children=[
                              html.H6(
                                  "Select tables that will be mapped to nodes"),
                              html.Button("ACTIVATE", id="activate-nodes"),
                              html.P("Not activated", id="nodes-activated")
                          ]), ]),
                      html.Div(id="functoriality-satisfied"),
                      html.Button("SUBMIT", style={
                                  "display": "none"}, id="submit-tables-to-nodes")
                      ]
        )
    ]


def notify_db_not_empty():
    if not graph_db.is_empty():
        return html.Div(id="proceed-with-nonempty-db", style={"margin": "10px", "border": "1px solid white"}, children=[
            html.P("The graph database is not empty. How do you want to proceed?"),
            html.Button("Empty the graph database", id="empty-graph-db"),
            html.Button("Append to the graph database", id="append-graph-db")])
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
    [Output("postgres-schema-container", "children"),
     Output("data-transformation-definition", "style")],
    [Input("load-schema-postgres", "n_clicks")],
)
def handle_not_empty_database_button(click1):
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "load-schema-postgres":
            return construct_postgres_schema(rel_db), {"display": "block"}
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback(
    [Output("edges-activated", "children"),
     Output("source-activated", "children"),
     Output("target-activated", "children"),
     Output("nodes-activated", "children"), 
     Output("rel-schema-cytoscape-result", "stylesheet")],
    [Input("activate-edges", "n_clicks"),
     Input("activate-source", "n_clicks"),
     Input("activate-target", "n_clicks"),
     Input("activate-nodes", "n_clicks")],
)
def handle_not_empty_database_button(click1, click2, click3, click4):
    ctx = dash.callback_context
    global currently_selected
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "activate-edges":
            global tables_to_edges
            currently_selected = tables_to_edges
            return "Activated", "Not activated", "Not activated", "Not activated", generate_stylesheet()
        elif prop_id == "activate-source":
            global source_fun
            currently_selected = source_fun
            return "Not activated", "Activated", "Not activated", "Not activated", generate_stylesheet()
        elif prop_id == "activate-target":
            global target_fun
            currently_selected = target_fun
            return "Not activated", "Not activated", "Activated", "Not activated", generate_stylesheet()
        elif prop_id == "activate-nodes":
            global tables_to_nodes
            currently_selected = tables_to_nodes
            return "Not activated", "Not activated", "Not activated", "Activated", generate_stylesheet()
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


def generate_stylesheet():
    global currently_selected
    default_stylesheet = [
        {
            'selector': 'node',
            'style': {
                        'content': 'data(label)',
                        'color': 'black'
            }
        },
        {
            'selector': 'edge',
            'style': {
                        'color': 'black',
                        'curve-style': 'bezier',
                        'target-arrow-shape': 'triangle'
            }
        }
    ]
    for elem in currently_selected:
        if "source" in elem.keys():
            sheet = {
                "selector": 'edge[id= "{}"]'.format(elem['id']),
                "style": {
                    "mid-target-arrow-color": '#B10DC9',
                    "mid-target-arrow-shape": "vee",
                    "line-color": '#B10DC9',
                    'opacity': 0.9,
                    'z-index': 5000
                }
            }
            default_stylesheet.append(sheet)
        else:
            sheet = {
                "selector": 'node[id = "{}"]'.format(elem['data']['id']),
                "style": {
                    'background-color': '#B10DC9',
                    "border-color": "purple",
                    "border-width": 2,
                    "border-opacity": 1,
                    "opacity": 1,

                    "label": "data(label)",
                    "color": "#B10DC9",
                    "text-opacity": 1,
                    "font-size": 12,
                    'z-index': 9999
                }
            }
            default_stylesheet.append(sheet)

    return default_stylesheet


@app.callback(
    [Output("functoriality-satisfied", "children"),
     Output("submit-tables-to-nodes", "style")],
    [Input("start-transformation-building", "n_clicks")],
)
def construct_functor():
    try:
        domain, fun, target = construct_functor(
            tables_to_nodes, tables_to_edges, source_fun, target_fun)
        global functor
        functor = Functor("transformation", domain, fun, target)
        return html.P("Transformation satisfies functoriality and is valid. Transformation can be executed."), {"display": "block"}
    except FunctorError:
        return html.P("The transformation does not satify functoriality. Select or deselect tables and relationships."), {"display": "none"}
