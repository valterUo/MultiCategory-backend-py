import dash
import dash_core_components as dcc
import dash_html_components as html


def model_tranformation_tab():
    return dcc.Tab(
        id="Model-transformation-tab",
        label="ModelTransformations",
        value="tab5",
        className="custom-tab",
        selected_className="custom-tab--selected",
    )


def build_model_tranformation_tab(state):
    return [
        html.Div(
            id="set-specs-intro-container",
            children=html.P(
                "This area is for creating selective queries and creating new objects and morphisms to the selected multi-model database."
            ),
        ),
    ]