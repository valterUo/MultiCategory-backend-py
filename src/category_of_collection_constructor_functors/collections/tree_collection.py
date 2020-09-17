import shelve
import os
import json
import pickle
from shelve import DbfilenameShelf
from json import JSONDecodeError
from supportive_functions.xml_to_dict import XmlDictConfig, XmlListConfig
import xml.etree.cElementTree as ET
from category_of_collection_constructor_functors.collections.collection_errors import FormatNotSupportedError

class TreeCollection:

    def __init__(self, name, source_file = None, target_folder = None, data_format = "JSON", target_file_path = None):
        self.name = name
        self.source_file = source_file
        self.target_folder = target_folder
        self.format = data_format
        if target_file_path == None:
            self.target_file_path = self.target_folder + "//" + self.name
        else:
            self.target_file_path = target_file_path
        if not os.path.isfile(self.target_file_path + ".dat"):
            if self.format == "JSON":
                self.parse_json()
            elif self.format == "XML":
                self.parse_xml()
            else:
                raise FormatNotSupportedError("The format is not supported", self.format)

    def get_name(self):
        return self.name

    def get_model(self):
        return "tree"

    def get_source_file(self):
        return self.source_file

    def get_target_folder(self):
        return self.target_folder

    def get_format(self):
        return self.format

    def get_target_file_path(self):
        return self.target_file_path

    ## This is problematic function for trees: we would like to iterate over all the nodes and the root
    ## but this is not wanted always and there is no unique identifier for all the elements and objects. 
    ## Thus it would be the best to find some "selection" method to pick efficiently right nodes
    ## among all the nodes. This can be tought also such way that we first perform a selective query and we iterate the result.
    def get_iterable_collection_of_objects(self, list_of_attributes = None):
        if list_of_attributes == None:
            return self.get_tree()
        else:
            result = []
            for attribute in list_of_attributes:
                result = result + self.find_elements_with_attribute(attribute)
            return result

    def save_to_shelve(self, data_set):
        d = shelve.open(self.target_file_path)
        if type(data_set) == dict:
            for key in data_set.keys():
                d[key] = data_set[key]
        elif type(data_set) == list:
            for i in range(len(data_set)):
                d[str(i)] = data_set[i]
        d.close()

    def parse_json(self):
        with open(self.source_file) as json_file:
            data_set = self.parse_json_file(json_file)
            self.save_to_shelve(data_set)
        
    def parse_json_file(self, json_file):
        data_set = None
        try:
            data_set = json.load(json_file)
        except JSONDecodeError:
            print("JSON Decoder Error. Trying read line by line.")
            try:
                data_set = []
                json_file.seek(0,0)  
                for json_line in json_file.readlines():
                    parsed_line = json.loads(json_line)
                    data_set.append(parsed_line)
            except Exception as e:
                print("JSON file is invalid: ", e)
        return data_set

    def parse_xml(self):
        tree = ET.parse(self.source_file)
        root = tree.getroot()
        xmldict = XmlListConfig(root)
        print({ root.tag: xmldict })
        self.save_to_shelve({ root.tag: xmldict })

    def get_tree(self):
        data = shelve.open(self.target_file_path)
        return data

    def find_elements_with_attribute(self, attribute, tree = None):
        result = []
        if tree == None:
            tree = self.get_tree()
        if type(tree) == dict or type(tree) == XmlDictConfig or type(tree) == DbfilenameShelf:
            for key in tree:
                if key == attribute:
                    if type(tree[key]) == list or type(tree[key]) == XmlListConfig:
                        result = result + tree[key]
                    else:
                        result.append(tree[key])
                result = result + self.find_elements_with_attribute(attribute, tree[key])
        elif type(tree) == list or type(tree) == XmlListConfig:
            for elem in tree:
                result = result + self.find_elements_with_attribute(attribute, elem)
        return result

    def find_elements_with_attribute_and_path(self, attribute, path, tree = None):
        result = []
        if tree == None:
            tree = self.get_tree()
        if type(tree) == dict or type(tree) == XmlDictConfig or type(tree) == DbfilenameShelf:
            for key in tree:
                if key == attribute:
                    if type(tree[key]) == list or type(tree[key]) == XmlListConfig:
                        i = 0
                        for elem in tree[key]:
                            result.append((elem, path + "/" + key + "/" + str(i)))
                            i+=1
                    else:
                        result.append((tree, path + "/" + key))
                result = result + self.find_elements_with_attribute_and_path(attribute, path + "/" + key, tree[key])
        elif type(tree) == list or type(tree) == XmlListConfig:
            i = 0
            for elem in tree:
                result = result + self.find_elements_with_attribute_and_path(attribute, path + "/" + str(i), elem)
                i+=1
        return result

    def append_to_collection(self, new_data_point):
        if self.target_file_path == None:
            self.target_file_path = self.target_folder_path + "//" + self.name + ".pyc"
        
        d = shelve.open(self.target_file_path)

        if type(new_data_point) == list or type(new_data_point) == XmlListConfig:
            if len(new_data_point) > 0:
                if len(new_data_point) > 1:
                    for i in range(len(new_data_point)):
                        d[str(i)] = new_data_point[i]
                elif type(new_data_point[0]) == dict or type(new_data_point) == XmlDictConfig:
                    for key in new_data_point[0]:
                        d[key] = new_data_point[key]
        elif type(new_data_point) == dict or type(new_data_point) == XmlDictConfig:
            for key in new_data_point:
                d[key] = new_data_point[key]

    def get_length(self):
        if self.target_file_path != None:
            d = shelve.open(self.target_file_path)
            return len(d.keys())
        else:
            return 0
        