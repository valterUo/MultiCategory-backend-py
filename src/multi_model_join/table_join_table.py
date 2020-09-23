from category_of_collection_constructor_functors.collections.table_collection import TableCollection
from category_of_collection_constructor_functors.collection_constructor import CollectionConstructor
from multi_model_join.model_category_join import ModelCategoryJoin
from tables import *
from supportive_functions.compositions import merge_two_dicts
from multi_model_join.helper_functions.parse_info import parse_info_for_join
from multi_model_join.helper_functions.create_h5_file import create_h5file

def table_join_table(first_collection_constructor, collection_constructor_morphism, second_collection_constructor, left = False):
    name, first_collection, first_model, collection_relationship, model_relationship, second_collection, second_model, first_file_path, result_file_name = parse_info_for_join(
        first_collection_constructor, collection_constructor_morphism, second_collection_constructor)

    first_collection_description = first_collection.get_attributes_datatypes_dict()
    second_collection_description = second_collection.get_attributes_datatypes_dict()
    length_of_first_collection_description = len(first_collection_description)
    result_description = merge_two_dicts(first_collection_description, second_collection_description)
    second_file_path = second_collection.get_target_file_path()
    result_collection, result_table_row, result_h5file = create_h5file(result_description, first_file_path, second_file_path, collection_constructor_morphism)
    objects = first_collection.get_iterable_collection_of_objects()

    for elem in objects:
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
        elif len(result_list) == 0 and left == True:
            for key in result_description:
                ## If we do not set values for all the columns in a row, the predefined default value is used which serves as NULL.
                    if j < length_of_first_collection_description:
                        result_table_row[key] = elem[key]

    result_h5file.close()
    result_model = ModelCategoryJoin(first_model, model_relationship, second_model)
    result = CollectionConstructor(name, result_model.get_result(), result_collection)
    return result, result_model