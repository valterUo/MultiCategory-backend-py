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

                 The target model can be 'ordinary' data models such as relational and graph. On the other hand, the target model
                 can also be String, Int or Boolean. In this case the query works as aggregation and the user needs to be sure that the result from the lambda function can be aggregated correctly. 
                 In this case user needs to define how the results are aggregated: this can be summing, multiplying, taking conjunctions or disjunctions.

                 This results that there are no aggregate functions implemented since all the simple aggregate functions can be written shortly using lambda notation. This might be useful to change in the future.

                Precisely, the both query evaluation mechanisms are similar but with different cons and nil values. In some cases cons function is known from the context but when we append, 
                for example, integers, we can append them multiple ways so there is no default cons function for this.

                 After this, the user composes the whole query by building these blocks. Any result of a block can be included into the final result. 
                 """
                            )
                        ),
                    ),
                ],
            )
        ),
    )