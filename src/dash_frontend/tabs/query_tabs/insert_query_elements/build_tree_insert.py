import dash_core_components as dcc
import dash_html_components as html
from dash_frontend.state.initialize_demo_state import state
from dash_frontend.server import app
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

def build_tree_insert(root, collection_constructor):
    return html.Div(id = "tree-insert-main-container", children = [

    ])