from category_of_collection_constructor_functors.collections.tree_collection import TreeCollection
from category_of_collection_constructor_functors.collection_constructor import CollectionConstructor
from multi_model_join.model_category_join import ModelCategoryJoin
from tables import *
from supportive_functions.compositions import merge_two_dicts
from multi_model_join.file_path_functions import parse_file_path
from multi_model_join.helper_functions.parse_info import parse_info_for_join
import shelve
from multi_model_join.tree_manipulation_functions import update, remove

def tree_join_tree(first_collection_constructor, collection_constructor_morphism, second_collection_constructor, left, attributes):
    name, first_collection, first_model, collection_relationship, model_relationship, second_collection, second_model, first_file_path, result_file_name = parse_info_for_join(
        first_collection_constructor, collection_constructor_morphism, second_collection_constructor)
    result_path = parse_file_path(first_file_path, result_file_name)
    result = shelve.open(result_path)
    ## First we create a copy of the original tree:
    all_objects = first_collection.get_iterable_collection_of_objects()
    for key in all_objects.keys():
        result[key] = all_objects[key]

    ## Then we store the result
    result_collection = TreeCollection(result_file_name, target_file_path = result_path)

    ## After this we modify the copy so that the orginal data are not affected
    objects = []
    for attribute in attributes:
        result_objects = result_collection.find_elements_with_attribute_and_path(attribute, "")
        if len(result_objects) == 0:
            raise Exception("No nodes for the given attributes.", attributes)
        else:
            objects = objects + result_objects
    for pair in objects:
        ## Each element consists of the node that has the attribute that the user gave and also a path to that element in the tree.
        ## The path gives a unique and relatively fast way to access the element again and substitute the new value into the tree.
        ## Unlike graphs and tables, trees do not have unique id system in this demo.
        elem, path = pair[0], pair[1]
        print(elem, path)
        result_list = collection_relationship.get_relationship(elem)
        print(result_list)
        if len(result_list) > 0:
            new_elem = dict()
            for elem2 in result_list:
                #print(elem2)
                new_elem = merge_two_dicts(new_elem, merge_two_dicts(elem, elem2[len(elem2) - 1]))
                print(path, new_elem)
            update(result, path, new_elem)
        elif len(result_list) == 0 and left == False:
            remove(path, result)

    result_model = ModelCategoryJoin(first_model, model_relationship, second_model, left)
    return CollectionConstructor(name, result_model.get_result(), result_collection), result_model