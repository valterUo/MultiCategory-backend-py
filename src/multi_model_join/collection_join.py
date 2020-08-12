from category_of_collection_constructor_functors.collections.graph_collection import GraphCollection
from category_of_collection_constructor_functors.collections.table_collection import TableCollection
from category_of_collection_constructor_functors.collections.tree_collection import TreeCollection

def join(first_collection, collection_relationship, second_collection):
    join_name = first_collection.get_name() + " + " + second_collection.get_name()
    if type(first_collection) == TableCollection:
        result = TableCollection(join_name, )
    elif type(first_collection) == GraphCollection:
        result = GraphCollection(join_name, )
    elif type(first_collection) == TreeCollection:
        result = TreeCollection(join_name, )
    return None

def execute_morphism(first_collection, collection_relationship, second_collection):
    for elem in first_collection.get_iterable_collection_of_objects():
        result_list = collection_relationship.get_relationship(elem)
        ## For every element in result_list we append the element in the first collection
        ## If the result is empty, then the collection stays the same