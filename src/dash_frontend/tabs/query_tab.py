import dash
import dash_core_components as dcc
import dash_html_components as html
from dash_frontend.state.initialize_demo_state import state


def query_tab():
    return dcc.Tab(
        id="Query-tab",
        label="Queries",
        value="tab3",
        className="custom-tab",
        selected_className="custom-tab--selected",
    )


def build_query_tab():
    #objects = state.get_current_state()["db"].get_objects()
    #print(objects)
    return [html.Div(id="query-tab-main-container", children=[
        html.Div(
            id="set-specs-intro-container",
            children=[
                html.P(
                    "This area is for creating selective queries and creating new objects and morphisms to the selected multi-model database."
                ),
                html.P("Visualize the whole selected dataset: "),
                dcc.Dropdown(
                    id="select-all-query-dropdown",
                    style={'width': '50%'},
                    options=[],
                ), html.Br(),
        html.Div(
            id="folding-tool",
            children=[
                html.P("Create a new collection and morphism from an existing collection.")
            ]
        ), html.Br(),
        html.Div(
            id="create-new-morphism-functor-tool",
            children=[
                html.P("Create a new morphism between existing collections.")
            ]
        ), html.Br(), 
        html.Div(
            id="create-new-collection-constructor-functor-tool",
            children=[
                html.P("Create a new (empty) collection constructor functor.")
            ]
        ),
    ])]
)]
