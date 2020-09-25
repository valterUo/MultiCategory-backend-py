from category_of_collection_constructor_functors.collections.table_collection import TableCollection
from category_of_collection_constructor_functors.collections.graph_collection import GraphCollection
from category_of_collection_constructor_functors.collections.tree_collection import TreeCollection
from category_of_collection_constructor_functors.collection_constructor import CollectionConstructor
from category_of_collection_constructor_functors.model_categories.converged_model_category_connection import ConvergedModelCategoryConnection

def construct_converged_collection_constructor_functor(name, model_categories, added_connections, target_folder_path):
    new_connections = []
    for connection in added_connections:
        domain = connection[0]
        target = connection[1]
        found_domain, found_target, found_domain_id, found_target_id = None, None, None, None
        for model_category in model_categories:
            for obj in model_category.get_objects():
                if domain == str(obj.get_id()):
                    found_domain = model_category
                    found_domain_id = domain
                if target == str(obj.get_id()):
                    found_target = model_category
                    found_target_id = target
                    
        new_connection = ConvergedModelCategoryConnection(found_domain, found_domain_id, found_target, found_target_id)
        new_connections.append(new_connection)
        found_domain.add_converged_model_categories(new_connection)

    root = None
    for model_category in model_categories:
        for new_connection in new_connections:
            if model_category == new_connection.get_target_model_category():
                break
        else:
            root = model_category

    root_collection = construct_collection(name, root, target_folder_path)
    result = CollectionConstructor(name, root, root_collection)
    return result

def construct_collection(name, root, target_folder_path):
    model = root.get_model()
    root_collection = None
    if model == "relational":
        root_collection = TableCollection(name, h5file_path=target_folder_path + "\\" + name + ".h5")
    elif model == "graph":
        root_collection = GraphCollection(name, target_folder_path=target_folder_path)
    elif model == "tree":
        root_collection = TreeCollection(name, target_file_path=target_folder_path)
    root_collection.add_converged_collections(name + "_sub", root.get_converged_model_categories(), target_folder_path)
    return root_collection