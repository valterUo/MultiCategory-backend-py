from category_of_collection_constructor_functors.model_categories.category_of_table_model import TableModelCategory
from category_of_collection_constructor_functors.model_categories.category_of_graph_model import GraphModelCategory
from category_of_collection_constructor_functors.model_categories.category_of_tree_model import TreeModelCategory
from category_of_collection_constructor_functors.model_categories.model_relationship import ModelRelationship

from category_of_collection_constructor_functors.collections.graph_collection import GraphCollection
from category_of_collection_constructor_functors.collections.table_collection import TableCollection
from category_of_collection_constructor_functors.collections.tree_collection import TreeCollection
from category_of_collection_constructor_functors.collections.collection_relationship import CollectionRelationship

from category_of_collection_constructor_functors.collection_constructor import CollectionConstructor
from category_of_collection_constructor_functors.collection_constructor_morphism import CollectionConstructorMorphism

import os
from tables import StringCol, tableextension
from supportive_functions.row_manipulations import row_to_dictionary_with_selection
from supportive_functions.xml_to_dict import XmlDictConfig, XmlListConfig
from dash_frontend.state.initialize_demo_state import state

"""
Input: source_dataset, filtering_condition, target_model
Source dataset: collectionConstructor
filtering_condition: python lambda function in string format
target_model: string
"""

class Fold:

    def __init__(self, name, source_dataset_name, filtering_condition, return_info, target_model):
        self.name = name
        self.source_dataset = state.get_current_state()["db"].get_objects()[source_dataset_name]
        self.filtering_condition = filtering_condition
        self.return_info = return_info
        self.target_model = target_model
        self.result = None
        self.result_morphism = None

        compiled_filtering_condition = compile(self.filtering_condition, 'filter.py', 'eval')
        self.filter_function = eval(compiled_filtering_condition)

        source_file_path = self.source_dataset.get_collection().get_target_file_path()
        base = os.path.dirname(os.path.abspath(source_file_path))
        #print(base)

        # create initial empty target model data set
        collection, model_category = None, None
        if self.target_model == "relational":
            result_file_path = base + "//" + self.name + ".h5"
            attributes_datatypes_dict = extract_attributes_datatypes_dict(self.source_dataset, return_info)
            collection = TableCollection(self.name, h5file_path=result_file_path, attributes_datatypes_dict=attributes_datatypes_dict)
            model_category = TableModelCategory(self.name, self.return_info)
        elif self.target_model == "graph":
            collection = GraphCollection(self.name, target_folder_path=base)
            model_category = GraphModelCategory(self.name, return_info["vertex_object_attributes"], return_info["edge_object_attributes"])
        elif self.target_model == "tree":
            collection = TreeCollection(self.name, target_folder=base)
            model_category = TreeModelCategory(self.name, return_info)
        
        self.result = CollectionConstructor(self.name, model_category, collection)
        whole_result = []
        for elem in self.source_dataset.get_iterable_collection_of_objects():
            if self.filter_function(elem):
                #print("Type of the result: " + str(type(elem)))
                #print(type(elem) == tuple)
                if type(elem) == tableextension.Row:
                    whole_result.append(row_to_dictionary_with_selection(elem, return_info))
                elif type(elem) == dict or type(elem) == XmlDictConfig:
                    whole_result.append(select(elem, return_info))
                elif type(elem) == tuple:
                    whole_result.append(select_from_tuple(elem, return_info))

        self.result.append_to_collection(whole_result)
        state.get_current_state()["db"].add_object(self.result)
    
    def get_result(self):
        return self.result

    def get_result_name(self):
        return self.result.get_name()
    
    def get_name(self):
        return self.name

    def get_model(self):
        return self.result.get_model()


def extract_attributes_datatypes_dict(source_dataset, return_info):
    attributes_datatypes_dict = dict()
    if source_dataset.get_model() == "relational":
        full_attributes_datatypes_dict = source_dataset.get_collection().get_attributes_datatypes_dict()
        for return_attribute in return_info:
            try:
                attributes_datatypes_dict[return_attribute] = full_attributes_datatypes_dict[return_attribute]
            except:
                print("Attribute" + return_attribute + " defined in RETURN clause is not in the domain table. Nothing is returned for this attribute.")
    else:
        for return_attribute in return_info:
            ## This might require some additional input from the user
            attributes_datatypes_dict[return_attribute] = StringCol(32)

    return attributes_datatypes_dict


def select(dictionary, return_info):
    selection = dict()
    for key in dictionary:
        if type(return_info) == list:
            if key in return_info:
                selection[key] = dictionary[key]
        elif type(return_info) == dict:
            values = []
            for value in return_info.values():
                values = values + value
            if key in values:
                selection[key] = dictionary[key]
    return selection

def select_from_tuple(tupl, return_info):
    selection = dict()
    obj = tupl[len(tupl) - 1]
    for key in obj:
        if type(return_info) == list:
            if key in return_info:
                selection[key] = obj[key]
        elif type(return_info) == dict:
            values = []
            for value in return_info.values():
                values = values + value
            if key in values:
                selection[key] = obj[key]
    if len(tupl) == 2:
        return (tupl[0], selection)
    elif len(tupl) == 3:
        return (tupl[0], tupl[1], selection)