from category_of_collection_constructor_functors.collections.graph_collection import GraphCollection
from category_of_collection_constructor_functors.collections.table_collection import TableCollection
from category_of_collection_constructor_functors.collections.tree_collection import TreeCollection
from category_of_collection_constructor_functors.collection_constructor import CollectionConstructor
import os
import numpy
from tables import *
from copy import deepcopy

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

def execute_collection_constructor_morphism(first_collection_constructor, collection_constructor_morphism, second_collection_constructor):
    collection_relationship = collection_constructor_morphism.get_collection_relationship()

    first_collection = first_collection_constructor.get_collection()
    first_model = first_collection_constructor.get_model_category()

    second_collection = second_collection_constructor.get_collection()
    second_model = second_collection_constructor.get_model_category()
    
    
    if type(first_collection) == TableCollection:
        first_collection_description = first_collection.get_attributes_datatypes_dict()
        first_old_h5_file_path = first_collection.get_h5file_path()
        first_file_name = parse_file_name(first_old_h5_file_path) + "_" + collection_constructor_morphism.get_name() + "_domain"
        print(first_file_name)
        first_h5file_path = parse_file_path(first_old_h5_file_path, first_file_name)
        first_h5file = open_file(first_h5file_path, mode="w", title = first_file_name + " file")
        first_group = first_h5file.create_group("/", first_file_name, first_file_name + " information")
        first_table = first_h5file.create_table(first_group, first_file_name, first_collection_description, first_file_name + " table")
        domain_collection = TableCollection(first_file_name, first_collection_description, h5file_path = first_h5file_path)
    elif type(first_collection) == GraphCollection:
        return None
    elif type(first_collection) == TreeCollection:
        return None

    if type(second_collection) == TableCollection:
        second_collection_description = second_collection.get_attributes_datatypes_dict()
        second_old_h5_file_path = second_collection.get_h5file_path()
        second_file_name = parse_file_name(second_old_h5_file_path) + "_" + collection_constructor_morphism.get_name() + "_target"
        second_h5file_path = parse_file_path(second_old_h5_file_path, second_file_name)
        print(second_h5file_path)
        second_h5file = open_file(second_h5file_path, mode="w", title = second_file_name + " file")
        second_group = second_h5file.create_group("/", second_file_name, second_file_name + " information")
        second_table = second_h5file.create_table(second_group, second_file_name, second_collection_description, second_file_name + " table")
        target_collection = TableCollection(second_file_name, second_collection_description, h5file_path = second_h5file_path)
    elif type(second_collection) == GraphCollection:
        return None
    elif type(second_collection) == TreeCollection:
        return None

    first_table_row = first_table.row
    second_table_row = second_table.row
    i = 0
    objects = first_collection.get_iterable_collection_of_objects()
    for elem in objects:
        if i % 1000 == 0:
            print(i)
        i+=1
        result_list = collection_relationship.get_relationship(elem)
        if len(result_list) > 0:
            if type(first_collection) == TableCollection:
                for key in first_collection_description:
                    first_table_row[key] = elem[key]
                first_table_row.append()
            elif type(first_collection) == GraphCollection:
                return None
            elif type(first_collection) == TreeCollection:
                return None

            if type(second_collection) == TableCollection:
                for elem2 in result_list:
                    for key in second_collection_description:
                        second_table_row[key] = elem2[key]
                    second_table_row.append()
            elif type(second_collection) == GraphCollection:
                return None
            elif type(second_collection) == TreeCollection:
                return None
    
    first_h5file.close()
    second_h5file.close()
    domain_name = collection_constructor_morphism.get_name() + " domain"
    target_name = collection_constructor_morphism.get_name() + " target"

    domain = CollectionConstructor(domain_name, first_model, domain_collection)
    target = CollectionConstructor(target_name, second_model, target_collection)

    return {"domain": domain, "morphism": collection_constructor_morphism, "target": target}