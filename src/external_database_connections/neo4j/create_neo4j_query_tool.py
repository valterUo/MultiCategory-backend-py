import dash_core_components as dcc
import dash_html_components as html
from dash_frontend.server import app
from dash.dependencies import Input, Output, State

from external_database_connections.neo4j.neo4j import Neo4j
graph_db = Neo4j("ldbcsf1")

def create_neo4j_query_tool():
    return html.Div(id = "neo4j-main-query-tool-container", children = [
        dcc.Textarea(id = "neo4j-query-input", value = "MATCH (n) RETURN n LIMIT 25"),
        html.Button("RUN", id = "submit-query"),
        html.Div(id = "viz"),
        html.Div(id = "hidden")
    ])

app.clientside_callback(
    """
    function draw(n_clicks, query) {
            console.log(value)
            var config = {
                container_id: "viz",
                server_url: "bolt://localhost:7687",
                server_user: "neo4j",
                server_password: "0000",
                initial_cypher: query
            }

            var viz = new NeoVis.default(config);
            viz.render();
            return "Something"
        };
    """,
    Output('hidden', 'children'),
    [Input('submit-query', 'n_clicks')], 
    [State("neo4j-query-input", "value")]
)