import dash
import dash_core_components as dcc
import dash_html_components as html

datasets = [
    {'label': 'E-commerce dataset', 'value': 'ecommerce'},
    {'label': 'Patent dataset', 'value': 'patent'},
    {'label': 'Online market place', 'value': 'market_place'},
    {'label': 'Unibench small dataset', 'value': 'unibench_small'},
    {'label': 'University dataset', 'value': 'university'},
    {'label': 'Person dataset', 'value': 'person'},
    {'label': 'Film dataset', 'value': 'film'}
]


def define_settings_tab():
    return dcc.Tab(
        id="Settings-tab",
        label="Database Settings",
        value="tab1",
        className="custom-tab",
        selected_className="custom-tab--selected",
    )


def build_settings_tab(state):
    current_state = state.get_current_state()
    return [
        html.Div(
            id="set-specs-intro-container",
            children=[html.P(
                "Select the demo dataset. The default dataset is the e-commerce dataset."
            ),
                dcc.Dropdown(
                id="metric-select-dropdown",
                options=datasets,
                value=current_state["value"]
            ),
            ]
        ),
    ]
