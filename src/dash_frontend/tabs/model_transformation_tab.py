import dash
import dash_core_components as dcc
import dash_html_components as html


def model_tranformation_tab():
    return dcc.Tab(
        id="Model-transformation-tab",
        label="Model Transformations",
        value="tab5",
        className="custom-tab",
        selected_className="custom-tab--selected",
    )


def build_model_tranformation_tab():
    return [
        html.Div(
            id="set-specs-intro-container",
            children=html.P(
                "This area is for creating model transformations between the external databases as Postgres and Neo4j."
            ),
        ),
    ]