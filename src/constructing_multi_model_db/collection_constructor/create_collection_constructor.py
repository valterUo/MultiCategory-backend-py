from category_of_collection_constructor_functors.collections.table_collection import TableCollection
from category_of_collection_constructor_functors.collections.graph_collection import GraphCollection
from category_of_collection_constructor_functors.collections.tree_collection import TreeCollection
from category_of_collection_constructor_functors.model_categories.category_of_table_model import TableModelCategory
from category_of_collection_constructor_functors.model_categories.category_of_graph_model import GraphModelCategory
from category_of_collection_constructor_functors.model_categories.category_of_tree_model import TreeModelCategory
from category_of_collection_constructor_functors.collection_constructor import CollectionConstructor

def create_collection_constructors(config):
    objects = dict()
    for info in config:
        model = info["model"]
        if model == "graph":
            name = info["name"]
            model = GraphModelCategory(name, info["vertexModel"], info["edgeModel"])
            collection = GraphCollection(name, info["vertexInfo"], info["edgeInfo"], info["targetFolder"])
        elif model == "relational":
            name = info["name"]
            try:
                primary_key = info["primaryKey"]
            except:
                primary_key = None
            attributes_datatypes = info["attributes_datatypes"]
            model = TableModelCategory(name, list(attributes_datatypes.keys()), primary_key)
            collection = TableCollection(name, attributes_datatypes, info["sourceFile"], info["targetFolder"], info["delimiter"])
        elif model == "tree":
            name = info["name"]
            model = TreeModelCategory(name)
            collection = TreeCollection(name, info["sourceFile"], info["targetFolder"], info["format"])
        objects[name] = CollectionConstructor(name, model, collection)
    return objects