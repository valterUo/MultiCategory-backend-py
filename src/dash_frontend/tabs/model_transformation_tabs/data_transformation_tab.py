import dash
import dash_core_components as dcc
import dash_html_components as html
import os

from abstract_category.functor.functor import Functor
from abstract_category.functor.functor_error import FunctorError
from dash_frontend.server import app
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash_frontend.tabs.model_transformation_tabs.construct_postgres_schema import construct_postgres_schema
from external_database_connections.neo4j.neo4j import Neo4j
from external_database_connections.postgresql.postgres import Postgres

rel_db = Postgres("lcdbsf1")
graph_db = Neo4j("lcdbsf1")
tables_to_nodes, tables_to_edges, source_fun, target_fun = [], [], [], []
functor = None


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
                      html.Div(id="postgres-schema-container"), html.Br(),
                      html.Div(id="functoriality-satisfied"), html.Br(),
                      html.Div(id="data-transformation-definition"), html.Br(),
                      html.Button("SUBMIT", style={
                          "display": "none"}, id="submit-tables-to-nodes")]
        ), html.Br()
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
     Output("data-transformation-definition", "children")],
    [Input("load-schema-postgres", "n_clicks")],
)
def load_schema_from_postgres_button(click1):
    data_transformation_elements = [html.Div(id="tables_to_edges", style={"width": "24%", "padding": "5px", "display": "inline-block", 'float': 'left', "borderRight": "1px solid white", "borderLeft": "1px solid white", "borderTop": "1px solid white"}, children=[
        html.H6(
            "Select tables that will be mapped to edges"),
        html.Div(style={"display": "inline"}, children=[
            html.Button("ADD SELECTED TABLES",
                        id="add-selected-elements-edges"),
            html.Button(
                "RESET", id="reset-edges"),
        ]),
        html.Div(id="selected-tables-to-edges")
    ]),
        html.Div(id="source-function", style={"width": "25%", "padding": "5px", "display": "inline-block", 'float': 'left', "borderRight": "1px solid white", "borderTop": "1px solid white"}, children=[
            html.H6(
                "Select relationships that will be mapped to source function"),
            html.Div(style={"display": "inline"}, children=[
                html.Button("ADD SELECTED RELATIONSHIPS",
                            id="add-selected-elements-source"),
                html.Button(
                    "RESET", id="reset-source"),
            ]),
            html.Div(id="selected-edges-to-source")
        ]),
        html.Div(id="target-function", style={"width": "25%", "padding": "5px", "display": "inline-block", 'float': 'left', "borderRight": "1px solid white", "borderTop": "1px solid white"}, children=[
            html.H6(
                "Select relationships that will be mapped to target function"),
            html.Div(style={"display": "inline"}, children=[
                html.Button("ADD SELECTED RELATIONSHIPS",
                            id="add-selected-elements-target"),
                html.Button(
                    "RESET", id="reset-target"),
            ]),
            html.Div(id="selected-edges-to-target")
        ]),
        html.Div(id="tables_to_nodes", style={"width": "24%", "padding": "5px", "display": "inline-block", 'float': 'left', "borderRight": "1px solid white", "borderTop": "1px solid white"}, children=[
            html.H6(
                "Select tables that will be mapped to nodes"),
            html.Div(style={"display": "inline"}, children=[
                html.Button("ADD SELECTED TABLES",
                            id="add-selected-elements-nodes"),
                html.Button("RESET", id="reset-nodes"),
            ]),
            html.Div(id="selected-tables-to-nodes")
        ]),
    ]
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "load-schema-postgres":
            return construct_postgres_schema(rel_db), data_transformation_elements
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback([Output("selected-tables-to-edges", "children"),
               Output("selected-tables-to-nodes", "children"),
               Output("selected-edges-to-source", "children"),
               Output("selected-edges-to-target", "children"),
               Output("functoriality-satisfied", "children"),
               Output("submit-tables-to-nodes", "style")],
              [Input("add-selected-elements-edges", "n_clicks"),
               Input("add-selected-elements-nodes", "n_clicks"),
               Input("reset-edges", "n_clicks"),
               Input("reset-nodes", "n_clicks"),
               Input("add-selected-elements-source", "n_clicks"),
               Input("add-selected-elements-target", "n_clicks"),
               Input("reset-source", "n_clicks"),
               Input("reset-target", "n_clicks")],
              [State('rel-schema-cytoscape-result', 'selectedNodeData'),
               State('rel-schema-cytoscape-result', 'selectedEdgeData')])
def displaySelectedNodeData(click1, click2, click3, click4, click5, click6, click7, click8, data_list_tables, data_list_rels):
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        global tables_to_edges
        global tables_to_nodes
        global source_fun
        global target_fun
        if prop_id == "add-selected-elements-edges":
            if not data_list_tables:
                raise PreventUpdate
            tables_to_edges += data_list_tables
        elif prop_id == "add-selected-elements-nodes":
            if not data_list_tables:
                raise PreventUpdate
            tables_to_nodes += data_list_tables
        elif prop_id == "add-selected-elements-source":
            if not data_list_rels:
                raise PreventUpdate
            source_fun += data_list_rels
        elif prop_id == "add-selected-elements-target":
            if not data_list_rels:
                raise PreventUpdate
            target_fun += data_list_rels
        elif prop_id == "reset-edges":
            tables_to_edges = []
        elif prop_id == "reset-nodes":
            tables_to_nodes = []
        elif prop_id == "reset-source":
            source_fun = []
        elif prop_id == "reset-target":
            target_fun = []
        else:
            raise PreventUpdate
        edge_names = [elem["id"] + "\n" for elem in tables_to_edges]
        node_names = [elem["id"] + "\n" for elem in tables_to_nodes]
        source_fun_names = [elem["source"] + " --> " +
                            elem["target"] + "\n" for elem in source_fun]
        target_fun_names = [elem["source"] + " --> " +
                            elem["target"] + "\n" for elem in target_fun]
        functor_valid, submit_button = construct_functor_component()
        return ", ".join(edge_names), ", ".join(node_names), ", ".join(source_fun_names), ", ".join(target_fun_names), functor_valid, submit_button
    else:
        raise PreventUpdate


def construct_functor_component():
    try:
        domain, fun, target = construct_functor()
        global functor
        functor = Functor("transformation", domain, fun, target)
        return html.P("Transformation satisfies functoriality and is valid. Transformation can be executed."), {"display": "block"}
    except FunctorError as e:
        print(e)
        return html.P("The transformation does not satify functoriality. Select or deselect tables and relationships."), {"display": "none"}


def construct_functor():
    target = {"objects": ["nodes", "edges"], "morphisms": [{"source": "edges", "morphism": "source",
                                                            "target": "nodes"}, {"source": "edges", "morphism": "target", "target": "nodes"}]}
    domain, fun = dict(), dict()
    domain["objects"] = []
    domain["morphisms"] = []
    for table in tables_to_nodes:
        domain["objects"].append(table["id"])
        fun[table["id"]] = "nodes"
    for table in tables_to_edges:
        domain["objects"].append(table["id"])
        fun[table["id"]] = "edges"
    for rel in source_fun:
        domain["morphisms"].append(
            {"source": rel["target"], "morphism": (rel["fk"], rel["pk"]), "target": rel["source"]})
        fun[(rel["fk"], rel["pk"])] = "source"
    for rel in target_fun:
        domain["morphisms"].append(
            {"source": rel["target"], "morphism": (rel["fk"], rel["pk"]), "target": rel["source"]})
        fun[(rel["fk"], rel["pk"])] = "target"
    return domain, fun, target
