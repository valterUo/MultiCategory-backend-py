from category_of_collection_constructor_functors.collections.table_collection import TableCollection
from category_of_collection_constructor_functors.collection_constructor import CollectionConstructor
from multi_model_join.model_category_join import join as model_join
from tables import *
from supportive_functions.compositions import merge_two_dicts
from multi_model_join.file_path_functions import parse_file_name, parse_file_path

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

        first_old_h5_file_path = first_collection.get_target_file_path()
        second_old_h5_file_path = second_collection.get_target_file_path()

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
            if i % 1000 == 0 and i != 0:
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
        result_model = model_join(first_model, collection_constructor_morphism.get_model_relationship(), second_model)
        result = CollectionConstructor(result_file_name, result_model, result_collection)
        return result