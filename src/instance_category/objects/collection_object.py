from data_parsers.csv_parser import read_to_table, dump_big_file_into_pickle
import networkx as nx
from data_parsers.property_graph_parser import parseDirectedGraph
from data_parsers.xml_parser import *
from data_parsers.rdf_parser import RDFParser
from instance_category.objects.collection_object_error import CollectionObjectError
import json
from pathlib import Path
import os
import pickle


class CollectionObject:

    """ 
    – file: path to the files or a list of paths
    – fileformat: the format that the file follows i.e. csv, json, rdf
    – collection_type: relational, property graph, RDF graph, tree structure
    – name: name of the object
    – separator: if the file is csv, this field specifies the separator
    """

    def __init__(self, name, collection_type, datatype, access_to_iterable=lambda x: x, file_dictionary=None, collection=None):
        self.name = name
        self.collection_type = collection_type
        self.file_dictionary = file_dictionary
        self.collection = collection
        self.datatype = datatype
        self.access_to_iterable = access_to_iterable
        if self.file_dictionary != None:
            if self.check_file_size_in_bytes(file_dictionary["filePath"]) < 1875000:
                self.parse_small_file_in_memory()
            else:
                file_name = self.parse_db_file_name(file_dictionary["filePath"])
                if self.check_if_file_exists(file_name):
                    print(file_name)
                    self.collection = file_name
                else:
                    self.parse_big_file_on_disc(file_name)

    def parse_small_file_in_memory(self):
        if self.collection_type == "relational":
            table = self.file_dictionary
            if table["fileformat"] == "csv":
                self.collection = read_to_table(table["filePath"], table["separator"], table["schema"], table["keyAttribute"])
        elif self.collection_type == "property graph":
            self.collection = parseDirectedGraph(self.file_dictionary)
        elif self.collection_type == "XML":
            self.collection = parseXML(self.file_dictionary["filePath"])
        elif self.collection_type == "RDF":
            self.collection = RDFParser(self.file_dictionary["filePath"])
        elif self.collection_type == "JSON":
            with open(self.file_dictionary["filePath"]) as json_file:
                self.collection = json.load(json_file)
        else:
            raise CollectionObjectError(self.collection_type, "The collection type is not known.")

    def check_file_size_in_bytes(self, file_name):
        return Path(file_name).stat().st_size

    def parse_db_file_name(self, file_path):
        dir_name = os.path.dirname(file_path)
        base = os.path.basename(file_path)
        base_without_extension = os.path.splitext(base)[0]
        return dir_name + "\\" + base_without_extension + ".pyc"
        
    def check_if_file_exists(self, file_name):
        return os.path.isfile(file_name) 

    def parse_big_file_on_disc(self, file_name):
        if self.collection_type == "relational":
            table = file_dictionary
            if table["fileformat"] == "csv":
                data_set = read_to_table(table["filePath"], table["separator"], table["schema"], table["keyAttribute"])
                self.collection = dump_big_file_into_pickle(data_set, file_name)
        elif self.collection_type == "property graph":
            data_set = parseDirectedGraph(file_dictionary)
            self.collection = dump_big_file_into_pickle(data_set, file_name)
        elif self.collection_type == "XML":
            data_set = parseXML(file_dictionary["filePath"])
            self.collection = dump_big_file_into_pickle(data_set, file_name)
        elif self.collection_type == "RDF":
            data_set = RDFParser(file_dictionary["filePath"])
            self.collection = dump_big_file_into_pickle(data_set, file_name)
        elif self.collection_type == "JSON":
            with open(file_dictionary["filePath"]) as json_file:
                data_set = json.load(json_file)
            self.collection = dump_big_file_into_pickle(data_set, file_name)
        else:
            raise CollectionObjectError(self.collection_type, "The collection type is not known.")

    def get_collection(self):
        if type(self.collection) == str:
            with open(self.collection, "rb") as db_file:
                unpickled_collection = pickle.load(db_file)
                return unpickled_collection
        else:
            return self.collection

    def get_collection_type(self):
        return self.collection_type

    def getName(self):
        return self.name

    def getDatatype(self):
        return self.datatype

    def get_access_to_iterable(self):
        return self.access_to_iterable(self.collection)

    def __str__(self):
        if self.collection_type == "relational" or self.collection == "JSON":
            elems = ""
            if type(self.collection) == dict():
                for elem in self.collection.values():
                    elems += str(elem) + "\n"
                return elems
            else:
                for elem in self.collection:
                    elems += str(elem) + "\n"
                return elems
        elif self.collection_type == "property graph":
            edges = ""
            for edge in self.collection.edges:
                edges += str(edge) + "\n"
            return edges
        elif self.collection_type == "XML":
            toStringTree(self.collection)
        elif self.collection_type == "RDF":
            return str(self.collection)

    def findFromNodes(self, attribute, value):
        result = []
        for elem in self.collection.nodes():
            if (attribute, str(value)) in elem:
                result.append(elem)
        return result

    def findFromList(self, attribute, value):
        for elem in self.collection:
            if elem[attribute] == value:
                return elem
        return None

    def get_d3js_element(self):
        return { 'name': self.name, 'collectionType': self.collection_type, 'datatype': self.datatype }

    def __eq__(self, other):
        return self.name == other.name