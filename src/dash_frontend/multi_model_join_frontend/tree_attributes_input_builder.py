import dash
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
from dash_frontend.server import app
from dash.dependencies import Input, Output

def tree_attributes_input_builder(state_dict):
    html.Div()