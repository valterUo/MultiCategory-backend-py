from werkzeug.utils import html
from dash_frontend.tabs.query_tabs.insert_query_elements.build_relational_insert import build_relational_insert
from dash_frontend.tabs.query_tabs.insert_query_elements.build_tree_insert import build_tree_insert
from dash_frontend.tabs.query_tabs.insert_query_elements.build_graph_insert import build_graph_insert
collection_constructor = None

def build_insert_tool(dataset):
    global collection_constructor
    collection_constructor = dataset
    main_insert_tool_container_children = []
    root_collection_html = None

    if collection_constructor.get_model() == "relational":
        root_collection_html = build_relational_insert(collection_constructor)
    elif collection_constructor.get_model() == "graph":
        root_collection_html = build_graph_insert(collection_constructor)
    elif collection_constructor.get_model() == "tree":
        root_collection_html = build_tree_insert(collection_constructor)
    
    main_insert_tool_container_children.append(root_collection_html)
    main_insert_tool_container_children = main_insert_tool_container_children + walk_converged_collection_tree(collection_constructor)

    return html.Div(id = "insert-tool-main-container", children = main_insert_tool_container_children)

def walk_converged_collection_tree(root):
    html_tree = []
    for child_connection in root.get_converged_collections():
        child_collection = child_connection.get_target_collection()
        if child_collection.get_model() == "relational":
            child_collection_html = build_relational_insert(root, child_collection) 
        elif child_collection.get_model() == "graph":
            child_collection_html = build_graph_insert(root, child_collection)
        elif child_collection.get_model() == "tree":
            child_collection_html = build_tree_insert(root, child_collection)
        html_tree.append(child_collection_html)
        html_tree = html_tree + walk_converged_collection_tree(child_collection)
    return html_tree