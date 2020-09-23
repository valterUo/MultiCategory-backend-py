from tables import *
from multi_model_join.file_path_functions import parse_file_name, parse_file_path
from category_of_collection_constructor_functors.collections.table_collection import TableCollection

def create_h5file(result_description, first_file_path, second_file_path, collection_constructor_morphism):
    result_file_name = parse_file_name(first_file_path) + "_" + collection_constructor_morphism.get_name() + "_" + parse_file_name(second_file_path)
    result_h5file_path = parse_file_path(first_file_path, result_file_name)
    result_h5file = open_file(result_h5file_path, mode="w", title = result_file_name + " file")
    result_group = result_h5file.create_group("/", result_file_name, result_file_name + " information")
    result_table = result_h5file.create_table(result_group, result_file_name, result_description, result_file_name + " table")
    result_collection = TableCollection(result_file_name, result_description, h5file_path = result_h5file_path)
    result_table_row = result_table.row
    return result_collection, result_table_row, result_h5file