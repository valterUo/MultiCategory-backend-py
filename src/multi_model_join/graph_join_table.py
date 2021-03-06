from category_of_collection_constructor_functors.collections.graph_collection import GraphCollection
from category_of_collection_constructor_functors.collection_constructor import CollectionConstructor
from multi_model_join.model_category_join import ModelCategoryJoin
from tables import *
import networkx as nx
from supportive_functions.compositions import merge_two_dicts
import pickle
from multi_model_join.file_path_functions import parse_file_name, parse_file_path
from multi_model_join.helper_functions.parse_info import parse_info_for_join


def graph_join_table(first_collection_constructor, collection_constructor_morphism, second_collection_constructor, left=False):
    name, first_collection, first_model, collection_relationship, model_relationship, second_collection, second_model, first_file_path, result_file_name = parse_info_for_join(
        first_collection_constructor, collection_constructor_morphism, second_collection_constructor)
    G = nx.DiGraph()
    objects = first_collection.get_iterable_collection_of_objects()
    ## Now elem is either (vertex_id, dict) or (source_id, target_id, dict)
    ## The result is assumed to be a simple dictionary
    for elem in objects:
        result_list = collection_relationship.get_relationship(elem)
        if len(result_list) > 0:
            if len(elem) == 2:
                merged_dict = dict()
                for elem2 in result_list:
                    merged_dict = merge_two_dicts(
                        merged_dict, merge_two_dicts(elem[1], elem2))
                G.add_nodes_from([(elem[0], merged_dict)])
            elif len(elem) == 3:
                merged_dict = dict()
                for elem2 in result_list:
                    merged_dict = merge_two_dicts(
                        merged_dict, merge_two_dicts(elem[2], elem2))
                G.add_edges_from([(elem[0], elem[1], merged_dict)])
        elif len(result_list) == 0 and left == True:
            if len(elem) == 2:
                G.add_nodes_from([elem])
            elif len(elem) == 3:
                G.add_edges_from([elem])

    result_file_path = parse_file_path(first_file_path, result_file_name)
    nx.write_gpickle(G, result_file_path, protocol=pickle.HIGHEST_PROTOCOL)
    result_collection = GraphCollection(name)
    result_collection.set_target_file_path(result_file_path)
    
    result_model = ModelCategoryJoin(first_model, model_relationship, second_model, left)
    result = CollectionConstructor(name, result_model.get_result(), result_collection)
    return result, result_model
