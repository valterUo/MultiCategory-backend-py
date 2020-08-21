from category_of_collection_constructor_functors.collections.table_collection import TableCollection
from category_of_collection_constructor_functors.collection_constructor import CollectionConstructor
from multi_model_join.model_category_join import join as model_join
from tables import *
from supportive_functions.compositions import merge_two_dicts
from multi_model_join.file_path_functions import parse_file_name, parse_file_path
from supportive_functions.row_manipulations import find_values_from_tree

def table_join_tree(first_collection_constructor, collection_constructor_morphism, second_collection_constructor, second_description, left = False, right = False):
        collection_relationship = collection_constructor_morphism.get_collection_relationship()

        first_collection = first_collection_constructor.get_collection()
        first_model = first_collection_constructor.get_model_category()

        second_collection = second_collection_constructor.get_collection()
        second_model = second_collection_constructor.get_model_category()

        first_collection_description = first_collection.get_attributes_datatypes_dict()

        if len(set(first_collection_description.keys()).intersection(set(second_description.keys()))) > 0:
            print("Warning: The descriptions are not disjoint. This might cause problems in the evaluation.")
        
        result_description = merge_two_dicts(first_collection_description, second_description)
        length_of_first_collection_description = len(first_collection_description)

        first_file_path = first_collection.get_target_file_path()
        second_file_path = second_collection.get_target_file_path()

        result_file_name = parse_file_name(first_file_path) + "_" + collection_constructor_morphism.get_name() + "_" + parse_file_name(second_file_path)
        result_h5file_path = parse_file_path(first_file_path, result_file_name)
        result_h5file = open_file(result_h5file_path, mode="w", title = result_file_name + " file")
        result_group = result_h5file.create_group("/", result_file_name, result_file_name + " information")
        result_table = result_h5file.create_table(result_group, result_file_name, result_description, result_file_name + " table")
        result_collection = TableCollection(result_file_name, result_description, h5file_path = result_h5file_path)
        result_table_row = result_table.row

        i = 0
        objects = first_collection.get_iterable_collection_of_objects()
        for elem in objects:
            if i % 1000 == 0 and i != 0:
                print("Rows processed: " + str(i))

            result_list = collection_relationship.get_relationship(elem)
            #print(result_list)
            if len(result_list) > 0:
                ## Here we assume that every element in the result has a tree structure
                ## The tree structure is flattened so that each path from the root to a leaf is made a row
                ## From the row we pick the wanted elements defined in the second description parameter
                for elem2 in result_list:
                    j = 0
                    for key in result_description:
                        if j >= length_of_first_collection_description:
                            picked_values_from_tree = find_values_from_tree(elem2, key)
                            if len(picked_values_from_tree) == 0:
                                print("No value for " + str(key) + " in the subtree.")
                            elif len(picked_values_from_tree) > 1:
                                print("Warning! With key " + str(key) + " exist multiple values. The algorithm picks the first.")
                                result_table_row[key] = picked_values_from_tree[0]
                            else:
                                result_table_row[key] = picked_values_from_tree[0]
                        else:
                            result_table_row[key] = elem[key]
                        j+=1
                    result_table_row.append()
            elif len(result_list) == 0 and left == True:
                for key in result_description:
                    ## If we do not set values for all the columns in a row, the predefined default value is used which serves as NULL.
                        if j < length_of_first_collection_description:
                            result_table_row[key] = elem[key]
            i+=1

        result_h5file.close()
        result_model = model_join(first_model, collection_constructor_morphism.get_model_relationship(), second_model)
        result = CollectionConstructor(result_file_name, result_model, result_collection)
        return result