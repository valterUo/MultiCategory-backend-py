from multi_model_join.file_path_functions import parse_file_name, parse_file_path

def parse_info_for_join(first_collection_constructor, collection_constructor_morphism, second_collection_constructor):
    name = first_collection_constructor.get_name() + " ⨝ " + second_collection_constructor.get_name()
    collection_relationship = collection_constructor_morphism.get_collection_relationship()
    model_relationship = collection_constructor_morphism.get_model_relationship()
    first_collection = first_collection_constructor.get_collection()
    first_model = first_collection_constructor.get_model_category()
    second_collection = second_collection_constructor.get_collection()
    second_model = second_collection_constructor.get_model_category()
    first_file_path = first_collection.get_target_file_path()
    second_file_path = second_collection.get_target_file_path()
    result_file_name = parse_file_name(first_file_path) + "_" + collection_constructor_morphism.get_name() + "_" + parse_file_name(second_file_path)
    return name, first_collection, first_model, collection_relationship, model_relationship, second_collection, second_model, first_file_path, result_file_name