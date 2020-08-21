import shelve
import os
import json
import pickle
from json import JSONDecodeError
from supportive_functions.xml_to_dict import XmlDictConfig, XmlListConfig
import xml.etree.cElementTree as ET
from category_of_collection_constructor_functors.collections.collection_errors import FormatNotSupportedError

class TreeCollection:

    def __init__(self, name, source_file, target_folder, data_format = "JSON"):
        self.name = name
        self.source_file = source_file
        self.target_folder = target_folder
        self.format = data_format
        self.target_file_path = self.target_folder + "//" + self.name
        if not os.path.isfile(self.target_file_path + ".dat"):
            if self.format == "JSON":
                self.parse_json()
            elif self.format == "XML":
                self.parse_xml()
            else:
                raise FormatNotSupportedError("The format is not supported", self.format)

    def get_name(self):
        return self.name

    def get_source_file(self):
        return self.source_file

    def get_target_folder(self):
        return self.target_folder

    def get_format(self):
        return self.format

    def get_target_file_path(self):
        return self.target_file_path

    def get_iterable_collection_of_objects(self):
        return self.get_tree()

    def save_to_shelve(self, data_set):
        d = shelve.open(self.target_file_path)
        if type(data_set) == dict:
            for key in data_set.keys():
                d[key] = data_set[key]
        elif type(data_set) == list:
            for i in range(len(data_set)):
                d[i] = data_set[i]
        d.close()

    def parse_json(self):
        d = shelve.open(self.target_file_path)
        with open(self.source_file) as json_file:
            data_set = self.parse_json_file(json_file)
            self.save_to_shelve(data_set)
        
    def parse_json_file(self, json_file):
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
        self.save_to_shelve(xmldict)

    def get_tree(self):
        data = shelve.open(self.target_file_path)
        return data