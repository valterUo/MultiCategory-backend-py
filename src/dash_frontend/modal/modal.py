import dash
import dash_core_components as dcc
import dash_html_components as html

def generate_modal():
    return html.Div(
        id="markdown",
        className="modal",
        children=(
            html.Div(
                id="markdown-container",
                className="markdown-container",
                children=[
                    html.Div(
                        className="close-container",
                        children=html.Button(
                            "Close",
                            id="markdown_close",
                            n_clicks=0,
                            className="closeButton",
                        ),
                    ),
                    html.Div(
                        className="markdown-text",
                        children=dcc.Markdown(
                            children=(
                                """
                        ###### What is this prototype app about?

                        This app demonstrates how applied category could be used to create theoretical foundations for multi-model databases.

                        See [the documentation](https://multicategory.github.io/) for more details and tutorials.

                        ###### What does this app shows

                        This app shows how category theory can be used to model multi-model databases. The user can choose between various example datasets. 
                        We visualize the datasets with functorial framework using schema and instance categories which are connected with instance functor.

                        The demo application implements multi-model joins.


                    """
                            )
                        ),
                    ),
                ],
            )
        ),
    )