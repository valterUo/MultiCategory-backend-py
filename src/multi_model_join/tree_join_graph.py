from category_of_collection_constructor_functors.collections.tree_collection import TreeCollection
from category_of_collection_constructor_functors.collection_constructor import CollectionConstructor
from multi_model_join.model_category_join import join as model_join
from tables import *
from supportive_functions.compositions import merge_two_dicts
from multi_model_join.file_path_functions import parse_file_name, parse_file_path
from supportive_functions.row_manipulations import find_values_from_tree
import shelve

def tree_join_graph(first_collection_constructor, collection_constructor_morphism, second_collection_constructor, left, attributes):
        collection_relationship = collection_constructor_morphism.get_collection_relationship()

        first_collection = first_collection_constructor.get_collection()
        first_model = first_collection_constructor.get_model_category()

        second_collection = second_collection_constructor.get_collection()
        second_model = second_collection_constructor.get_model_category()

        first_file_path = first_collection.get_target_file_path()
        second_file_path = second_collection.get_target_file_path()

        result_file_name = parse_file_name(first_file_path) + "_" + collection_constructor_morphism.get_name() + "_" + parse_file_name(second_file_path)
        result_path = parse_file_path(first_file_path, result_file_name)
        
        result = shelve.open(result_path)

        ## First we create a copy of the original tree:
        all_objects = first_collection.get_iterable_collection_of_objects()
        for key in all_objects.keys():
            result[key] = all_objects[key]

        ## Then we store the result
        result_collection = TreeCollection(result_file_name, target_file_path = result_path)

        ## After this we modify the copy so that the orginal data are not affected
        i = 0
        objects = result_collection.find_elements_with_attribute_and_path(attributes, "")
        if len(objects) == 0:
            raise Exception("No nodes for the given attributes.", attributes)
        for pair in objects:
            if i % 1000 == 0 and i != 0:
                print("Nodes processed: " + str(i))
            ## Each element consists of the node that has the attribute that the user gave and also a path to that element in the tree.
            ## The path gives a unique and relatively fast way to access the element again and substitute the new value into the tree.
            ## Unlike graphs and tables, trees do not have unique id system in this demo.
            elem, path = pair[0], pair[1]
            result_list = collection_relationship.get_relationship(elem)
            print(result_list)
            if len(result_list) > 0:
                new_elem = dict()
                for elem2 in result_list:
                    new_elem = merge_two_dicts(new_elem, merge_two_dicts(elem, elem2))
                update(result, path, new_elem)
            elif len(result_list) == 0 and left == False:
                remove(path, result)
            i+=1

        result_model = model_join(first_model, collection_constructor_morphism.get_model_relationship(), second_model)
        result = CollectionConstructor(result_file_name, result_model, result_collection)
        return result


def path_get(mydict, path):
    elem = mydict
    try:
        for x in path.strip("/").split("/"):
            print(x)
            try:
                x = int(x)
                elem = elem[x]
            except:
                elem = elem.get(x)
    except:
        pass
    return elem

def update(mydict, path, new_elem):
    key_path = path.strip("/").split("/")
    if len(key_path) > 1:
        main_key = key_path.pop(0)
        last_key = key_path[-1]
        new_dict = dict(mydict[main_key])
        elem = new_dict
        for key in key_path:
            if key == last_key:
                try:
                    elem[key] = new_elem
                except:
                    pass
            else:
                try:
                    elem = new_dict[key]
                except:
                    pass
        mydict[main_key] = new_dict

def remove(mydict, path):
    key_path = path.strip("/").split("/")
    if len(key_path) > 1:
        main_key = key_path.pop(0)
        last_key = key_path[-1]
        new_dict = dict(mydict[main_key])
        elem = new_dict
        for key in key_path:
            if key == last_key:
                try:
                    del elem[key]
                except:
                    pass
            else:
                try:
                    elem = new_dict[key]
                except:
                    pass
        mydict[main_key] = new_dict