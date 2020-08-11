import shelve
import os
import json
import pickle
from json import JSONDecodeError
import xml.etree.cElementTree as ET
from category_of_collection_constructor_functors.collections.collection_errors import FormatNotSupportedError

class TreeCollection:

    def __init__(self, name, source_file, target_folder, data_format = "JSON"):
        self.name = name
        self.source_file = source_file
        self.target_folder = target_folder
        self.format = data_format
        self.target_file_name = self.target_folder + "//" + self.name + ".db"
        if not os.path.isfile(self.target_file_name):
            if self.format == "JSON":
                self.parse_json()
            elif self.format == "XML":
                self.parse_xml()
            else:
                raise FormatNotSupportedError("The format is not supported", self.format)

    def parse_json(self):
        d = shelve.open(self.target_file_name)
        with open(self.source_file) as json_file:
                data_set = self.parse_json_file(json_file)
        if type(data_set) == dict:
            for key in data_set.keys():
                d[key] = data_set[key]
        elif type(data_set) == list:
            for i in range(len(data_set)):
                d[i] = data_set[i]
        d.close()

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
        #parser = ET.XMLParser(encoding="utf-8")
        #tree = ET.fromstring(self.source_file, parser=parser)
        tree = ET.parse(self.source_file)
        with open(self.target_file_name, "wb+") as target_file:
            pickle.dump(tree, target_file, protocol=pickle.HIGHEST_PROTOCOL)

    def pretty_print(self):
        if self.format == "XML":
            tree = pickle.loads(self.target_file_name)
            for elem in tree.getroot().iter():
                print(elem.tag, elem.text)
        elif self.format == "JSON":
           data = shelve.open(self.target_file_name)
           for key in data:
                try:
                    print("Key: " + str(key) + ", ", "Value: " + str(data[key]))
                except:
                    print("JSON dictionary")

    def get_tree(self):
        if self.format == "JSON":
            data = shelve.open(self.target_file_name)
            return data
        elif self.format == "XML":
            tree = pickle.loads(self.target_file_name)
            return tree