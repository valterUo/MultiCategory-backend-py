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
        
        result_description = merge_two_dicts(first_collection_description, second_description)
        length_of_first_collection_description = len(first_collection_description)

        first_file_path = first_collection.get_target_file_path()
        second_file_path = second_collection.get_target_file_path()

        result_file_name = parse_file_name(first_file_path) + "_" + collection_constructor_morphism.get_name() + "_" + parse_file_name(second_file_path)
        result_path = parse_file_path(first_file_path, result_file_name)
        result = shelve.open(result_path)
        i = 0
        objects = first_collection.get_iterable_collection_of_objects(attributes)
        for elem in objects:
            if i % 1000 == 0 and i != 0:
                print("Nodes processed: " + str(i))

            result_list = collection_relationship.get_relationship(elem)
            print(result_list)
            if len(result_list) > 0:
                for elem2 in result_list:
                    
            elif len(result_list) == 0 and left == True:
                
            i+=1

        result_collection = TreeCollection(result_file_name, target_file_path = result_path)
        result_model = model_join(first_model, collection_constructor_morphism.get_model_relationship(), second_model)
        result = CollectionConstructor(result_file_name, result_model, result_collection)
        return result