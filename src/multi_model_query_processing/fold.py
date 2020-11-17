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
from shelve import DbfilenameShelf
from tables import StringCol, tableextension
from multicategory.initialize_multicategory import multicategory
from supportive_functions.row_manipulations import row_to_dictionary_with_selection
from supportive_functions.xml_to_dict import XmlDictConfig, XmlListConfig
from multi_model_query_processing.selection_functions import select, select_from_tuple
import re

"""
Input: source_dataset, filtering_condition, target_model
Source dataset: collectionConstructor
filtering_condition: python lambda function in string format
target_model: string
"""


class Fold:

    def __init__(self, name, source_dataset_name, filtering_condition, return_info, target_model):
        self.name = name
        self.source_dataset = multicategory.get_selected_multi_model_database().get_objects()[
            source_dataset_name]
        self.filtering_condition = filtering_condition
        self.return_info = return_info
        self.target_model = target_model
        self.result = None
        self.whole_result = []
        compiled_filtering_condition = compile(self.filtering_condition, 'filter.py', 'eval')
        self.filter_function = eval(compiled_filtering_condition)
        self.initialize_result()
        objects = self.source_dataset.get_iterable_collection_of_objects()
        self.query(objects)
        #print("Whole result: ", whole_result)
        self.result.append_to_collection(self.whole_result)
        self.commit_to_multi_model_database()

    def get_result(self):
        return self.result

    def get_result_name(self):
        return self.result.get_name()

    def get_name(self):
        return self.name

    def get_model(self):
        return self.result.get_model()

    def initialize_result(self):
        collection, model_category = None, None
        source_file_path = self.source_dataset.get_collection().get_target_file_path()
        base = os.path.dirname(os.path.abspath(source_file_path))
        if self.target_model == "relational":
            result_file_path = base + "//" + self.name + ".h5"
            attributes_datatypes_dict = self.extract_attributes_datatypes_dict()
            collection = TableCollection(self.name, h5file_path=result_file_path, attributes_datatypes_dict=attributes_datatypes_dict)
            model_category = TableModelCategory(self.name, self.return_info)
        elif self.target_model == "graph":
            collection = GraphCollection(self.name, target_folder_path=base)
            model_category = GraphModelCategory(self.name, self.return_info["vertex_object_attributes"], self.return_info["edge_object_attributes"])
        elif self.target_model == "tree":
            collection = TreeCollection(self.name, target_folder=base)
            model_category = TreeModelCategory(self.name, self.return_info)
        self.result = CollectionConstructor(self.name, model_category, collection)

    def commit_to_multi_model_database(self):
        multicategory.get_selected_multi_model_database().add_object(self.result)
        model_relation = self.construct_model_relation()
        model_rel = ModelRelationship(self.name, self.source_dataset.get_model_category(), model_relation, self.result.get_model_category())
        lambda_function = self.construct_lambda_function()
        collection_rel = CollectionRelationship(self.name, self.source_dataset.get_collection(), lambda_function, self.result.get_collection())
        mor = CollectionConstructorMorphism(self.name, self.source_dataset, model_rel, collection_rel, self.result)
        multicategory.get_selected_multi_model_database().add_morphism(mor)

    def filter(self, elem, objects=None):
        if type(elem) == tableextension.Row:
            return self.filter_function(elem)
        elif type(elem) == str and objects != None:
            if type(objects[elem]) == dict or type(objects[elem]) == XmlDictConfig or type(objects[elem]) == DbfilenameShelf or type(objects[elem]) == XmlListConfig:
                return self.filter_function(objects[elem])
        elif type(elem) == tuple:
            return self.filter_function(elem[-1])

    def query(self, objects):
        for elem in objects:
            if self.filter(elem, objects):
                if type(elem) == tableextension.Row:
                    self.whole_result.append(row_to_dictionary_with_selection(elem, self.return_info))
                elif type(elem) == str:
                    if type(objects[elem]) == dict or type(objects[elem]) == XmlDictConfig or type(objects[elem]) == XmlListConfig or type(elem) == DbfilenameShelf:
                        self.whole_result.append(select(objects, self.return_info, elem))
                elif type(elem) == tuple:
                    self.whole_result.append(select_from_tuple(elem, self.return_info, self.target_model))

    def extract_attributes_datatypes_dict(self):
        attributes_datatypes_dict = dict()
        if self.source_dataset.get_model() == "relational":
            full_attributes_datatypes_dict = self.source_dataset.get_collection(
            ).get_attributes_datatypes_dict()
            for return_attribute in self.return_info:
                try:
                    attributes_datatypes_dict[return_attribute] = full_attributes_datatypes_dict[return_attribute]
                except:
                    print("Attribute" + return_attribute +
                          " defined in RETURN clause is not in the domain table. Nothing is returned for this attribute.")
        else:
            if type(self.return_info) == list:
                for return_attribute in self.return_info:
                    ## This might require some additional input from the user
                    attributes_datatypes_dict[return_attribute] = StringCol(32)
            elif type(self.return_info) == dict:
                for key in self.return_info:
                    for attr in self.return_info[key]:
                        ## This might require some additional input from the user
                        attributes_datatypes_dict[attr] = StringCol(32)
        return attributes_datatypes_dict

    def construct_lambda_function(self):
        def result_function(x):
            if self.filter_function(x):
                return [x]
            else:
                return []
        return result_function

    def construct_model_relation(self):
        result = []
        split_result = re.findall(
            "(?<=\[)(.*?)(?=\])", self.filtering_condition)
        print(split_result)
        for elem in split_result:
            result.append({elem: elem})
        return result
