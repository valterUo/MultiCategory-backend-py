from category_of_collection_constructor_functors.collections.graph_collection import GraphCollection
from category_of_collection_constructor_functors.collections.table_collection import TableCollection
from category_of_collection_constructor_functors.collections.tree_collection import TreeCollection
from category_of_collection_constructor_functors.collection_constructor import CollectionConstructor
from multi_model_join.model_category_join import join as model_join
import numpy
import os
import networkx as nx
from supportive_functions.row_manipulations import row_to_dictionary
from supportive_functions.compositions import merge_two_dicts
import pickle

def graph_join_graph(first_collection_constructor, collection_constructor_morphism, second_collection_constructor, left = False):
        collection_relationship = collection_constructor_morphism.get_collection_relationship()

        first_collection = first_collection_constructor.get_collection()
        first_model = first_collection_constructor.get_model_category()

        second_collection = second_collection_constructor.get_collection()
        second_model = second_collection_constructor.get_model_category()

        first_file_path = first_collection.get_target_file_path()
        second_file_path = second_collection.get_target_file_path()
        result_file_name = parse_file_name(first_file_path) + "_" + collection_constructor_morphism.get_name() + "_" + parse_file_name(second_file_path)

        G = nx.DiGraph()

        i = 0
        objects = first_collection.get_iterable_collection_of_objects()
        ## Now elem is either (vertex_id, dict) or (source_id, target_id, dict)
        ## The result is assumed to be a simple dictionary

        for elem in objects:
            if i % 1000 == 0 and i != 0:
                print("Nodes or edges processed: " + str(i))

            result_list = collection_relationship.get_relationship(elem)
            if len(result_list) > 0:
                if len(elem) == 2:
                    merged_dict = dict()
                    for elem2 in result_list:
                        merged_dict = merge_two_dicts(merged_dict, merge_two_dicts(elem[1], elem2))
                    G.add_nodes_from([(elem[0], merged_dict)])
                elif len(elem) == 3:
                    merged_dict = dict()
                    for elem2 in result_list:
                        merged_dict = merge_two_dicts(merged_dict, merge_two_dicts(elem[2], elem2))
                    G.add_edges_from([(elem[0], elem[1], merged_dict)])
            elif len(result_list) == 0 and left == True:
                if len(elem) == 2:
                    G.add_nodes_from([elem])
                elif len(elem) == 3:
                    G.add_edges_from([elem])
            i+=1

        result_file_path = parse_file_path(first_file_path, result_file_name)
        nx.write_gpickle(G, result_file_path, protocol=pickle.HIGHEST_PROTOCOL)
        result_collection = GraphCollection(result_file_name)
        result_collection.set_target_file_path(result_file_path)
        result_model = model_join(first_model, collection_constructor_morphism.get_model_relationship(), second_model)
        result = CollectionConstructor(result_file_name, result_model, result_collection)
        return result