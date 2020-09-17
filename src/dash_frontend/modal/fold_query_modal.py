import dash
import dash_core_components as dcc
import dash_html_components as html

def generate_fold_query_modal():
    return html.Div(
        id="markdown-fold-query",
        className="modal",
        children=(
            html.Div(
                id="markdown-container-fold-query",
                className="markdown-container",
                children=[
                    html.Div(
                        className="close-container",
                        children=html.Button(
                            "Close",
                            id="markdown_close_fold",
                            n_clicks=0,
                            className="closeButton",
                        ),
                    ),
                    html.Div(
                        className="markdown-text",
                        children=dcc.Markdown(
                            children=( 
                                """
                 ###### Multi-model query processing               
                The following query mechanism utilizes fold-function. 
                 
                 For each query block user defines three parameters: the dataset where the query is execute (SQL equivalent 'FROM'), 
                 a model that the result will follow and a lambda function. Generally the lambda function would be an arbitrary Python lambda function but in this demo we allow only lambda functions
                 that define filtering condition. This means that the user defines a predicate P(x) for each object in the domain dataset that is queried. For example, this could be P(x) := (x == 'Mary') resulting
                 either True or False depending if x equals 'Mary'.

                 After this, the user composes the whole query by building these blocks. Any result of a block can be included into the final result. 
                 """
                            )
                        ),
                    ),
                ],
            )
        ),
    )