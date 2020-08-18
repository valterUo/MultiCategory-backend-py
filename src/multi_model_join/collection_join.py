from category_of_collection_constructor_functors.collections.graph_collection import GraphCollection
from category_of_collection_constructor_functors.collections.table_collection import TableCollection
from category_of_collection_constructor_functors.collections.tree_collection import TreeCollection
from category_of_collection_constructor_functors.collection_constructor import CollectionConstructor
from multi_model_join.model_category_join import join
import numpy
import os
from tables import *

## Morphisms between collection constructors are not automatically evaluated. They model relationships between different models.
## Because relationships generally are modelled as relations, this means that there is some amount of elements in the first collection
## that are in a relation with some elements in the second collection. As border cases it is possible that there is no element in the
## first collection that is in a relationship with any element in the second collection. On the other hand, the relationship does not need
## to be functional. Multi-model join means that we take pairs (a, b) in the relation and create a new element combining a and b and substitute
## it to the structure of a. The multi-model join works naturally in the sense that if a is not in relation with any b then a is not included
## in the result.

## It would be possible to create two morphisms from joined collections to the result collection. This needs to be implemented later.

def merge_two_dicts(x, y):
      z = x.copy()
      z.update(y)
      return z

def parse_file_path(old_path, new_file_name):
    dir_name = os.path.dirname(old_path)
    # base = os.path.basename(old_path)
    # filename = os.path.splitext(base)[0]
    file_extension = os.path.splitext(old_path)[1]
    return dir_name + "\\" + new_file_name + file_extension

def parse_file_name(path):
    base = os.path.basename(path)
    filename = os.path.splitext(base)[0]
    return filename

def join(first_collection_constructor, collection_constructor_morphism, second_collection_constructor):
    first_collection = first_collection_constructor.get_collection()
    second_collection = second_collection_constructor.get_collection()

    if type(first_collection) == TableCollection:
        if type(second_collection) == TableCollection:
            result = table_join_table(first_collection_constructor, collection_constructor_morphism, second_collection_constructor)
        elif type(second_collection) == GraphCollection:
            #result = table_join_graph(first_collection_constructor, collection_constructor_morphism, second_collection_constructor)
            result = None
        elif type(second_collection) == TreeCollection:
            #result = table_join_tree(first_collection_constructor, collection_constructor_morphism, second_collection_constructor)
            result = None
    elif type(first_collection) == GraphCollection:
        if type(second_collection) == TableCollection:
            result = graph_join_table(first_collection_constructor, collection_constructor_morphism, second_collection_constructor)
        elif type(second_collection) == GraphCollection:
            #result = graph_join_graph(first_collection_constructor, collection_constructor_morphism, second_collection_constructor)
            result = None
        elif type(second_collection) == TreeCollection:
             #esult = graph_join_tree(first_collection_constructor, collection_constructor_morphism, second_collection_constructor)
             result = None
    elif type(first_collection) == TreeCollection:
        if type(second_collection) == TableCollection:
            #result = tree_join_table(first_collection_constructor, collection_constructor_morphism, second_collection_constructor)
            result = None
        elif type(second_collection) == GraphCollection:
            #result = tree_join_graph(first_collection_constructor, collection_constructor_morphism, second_collection_constructor)
            result = None
        elif type(second_collection) == TreeCollection:
            #result = tree_join_tree(first_collection_constructor, collection_constructor_morphism, second_collection_constructor)
            result = None
    return result

def table_join_table(first_collection_constructor, collection_constructor_morphism, second_collection_constructor):
    collection_relationship = collection_constructor_morphism.get_collection_relationship()

    first_collection = first_collection_constructor.get_collection()
    first_model = first_collection_constructor.get_model_category()

    second_collection = second_collection_constructor.get_collection()
    second_model = second_collection_constructor.get_model_category()

    first_collection_description = first_collection.get_attributes_datatypes_dict()
    length_of_first_collection_description = len(first_collection_description)
    second_collection_description = second_collection.get_attributes_datatypes_dict()
    result_description = merge_two_dicts(first_collection_description, second_collection_description)

    first_old_h5_file_path = first_collection.get_h5file_path()
    second_old_h5_file_path = second_collection.get_h5file_path()

    result_file_name = parse_file_name(first_old_h5_file_path) + "_" + collection_constructor_morphism.get_name() + "_" + parse_file_name(second_old_h5_file_path)
    result_h5file_path = parse_file_path(first_old_h5_file_path, result_file_name)
    result_h5file = open_file(result_h5file_path, mode="w", title = result_file_name + " file")
    result_group = result_h5file.create_group("/", result_file_name, result_file_name + " information")
    result_table = result_h5file.create_table(result_group, result_file_name, result_description, result_file_name + " table")
    result_collection = TableCollection(result_file_name, result_description, h5file_path = result_h5file_path)
    result_table_row = result_table.row

    i = 0
    objects = first_collection.get_iterable_collection_of_objects()
    for elem in objects:
        if i % 1000 == 0:
            print("Rows processed: " + str(i))
        result_list = collection_relationship.get_relationship(elem)
        if len(result_list) > 0:
            for elem2 in result_list:
                j = 0
                for key in result_description:
                    if j >= length_of_first_collection_description:
                        result_table_row[key] = elem2[key]
                    else:
                        result_table_row[key] = elem[key]
                    j+=1
                result_table_row.append()
        i+=1

    result_h5file.close()
    result_model = join(first_model, collection_constructor_morphism.get_model_relationship(), second_model)
    result = CollectionConstructor(result_file_name, result_model, result_collection)
    return result

def graph_join_table(first_collection_constructor, collection_constructor_morphism, second_collection_constructor):
    return None