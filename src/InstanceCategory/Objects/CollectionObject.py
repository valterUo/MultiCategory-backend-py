from DataParsers.CSVParser import readToTable
import networkx as nx
from DataParsers.PropertyGraphParser import parseDirectedGraph
from DataParsers.XMLParser import *
from DataParsers.RDFParser import RDFParser
import json


class CollectionObject:

    """ 
    – file: path to the files or a list of paths
    – fileformat: the format that the file follows i.e. csv, json, rdf
    – collectionType: relational, property graph, RDF graph, tree structure
    – name: name of the object
    – separator: if the file is csv, this field specifies the separator
    """

    def __init__(self, name, collectionType, filePaths = None, fileformat = None, schema=None, keyAttribute=None, separator=";", edgeSchema=None, edgeKeyAttribute=None, fromKeyAttribute=None, toKeyAttribute=None):
        self.filePaths = filePaths
        self.fileformat = fileformat
        self.collectionType = collectionType
        self.name = name
        self.schema = schema
        if self.collectionType == "relational":
            if self.fileformat == "csv":
                self.collection = readToTable(
                    self.filePaths, separator, self.schema, keyAttribute)
        elif self.collectionType == "property graph":
            if self.fileformat == "csv":
                self.collection = parseDirectedGraph(
                    filePaths[0], filePaths[1], separator, separator, schema, edgeSchema, keyAttribute, edgeKeyAttribute, fromKeyAttribute, toKeyAttribute)
        elif self.collectionType == "XML":
            self.collection = parseXML(filePaths)
        elif self.collectionType == "RDF":
            self.collection = RDFParser(filePaths)
        elif self.collectionType == "JSON":
            with open(filePaths) as json_file:
                self.collection = json.load(json_file)

    def getCollection(self):
        return self.collection

    def getCollectionType(self):
        return self.collectionType

    def __str__(self):
        if self.collectionType == "relational" or self.collection == "JSON":
            elems = ""
            for elem in self.collection.values():
                elems += str(elem) + "\n"
            return elems
        elif self.collectionType == "property graph":
            edges = ""
            for edge in self.collection.edges:
                edges += str(edge) + "\n"
            return edges
        elif self.collectionType == "XML":
            toStringTree(self.collection)
        elif self.collectionType == "RDF":
            return str(self.collection)

    def findFromNodes(self, attribute, value):
        print(attribute, value)
        result = []
        for elem in self.collection.nodes():
            if (attribute, str(value)) in elem:
                result.append(elem)
        return result
