import dash
import dash_core_components as dcc
import dash_html_components as html


def create_morphism_subtab():

    return dcc.Tab(
        id="Create-morphism-subtab",
        label="Create morphism",
        value="subtab2",
        className="custom-tab",
        selected_className="custom-tab--selected",
    )


def build_create_morphism_subtab():
    return [html.Div()]
