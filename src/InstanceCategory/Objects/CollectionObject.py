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

    def __init__(self, name, collectionType, fileDictonaries = None, collection = None):
        self.name = name
        self.collectionType = collectionType
        self.fileDictonaries = fileDictonaries
        self.collection = collection
        if self.collectionType == "relational":
            table = fileDictonaries
            if table["fileformat"] == "csv":
                self.collection = readToTable(
                    table["filePath"], table["separator"], table["schema"], table["keyAttribute"])
        elif self.collectionType == "property graph":
            self.collection = parseDirectedGraph(fileDictonaries)
        elif self.collectionType == "XML":
            self.collection = parseXML(fileDictonaries["filePath"])
        elif self.collectionType == "RDF":
            self.collection = RDFParser(fileDictonaries["filePath"])
        elif self.collectionType == "JSON":
            document = fileDictonaries
            with open(document["filePath"]) as json_file:
                self.collection = json.load(json_file)


    def getCollection(self):
        return self.collection


    def setCollection(self, newcollection):
        self.collection = newcollection


    def getCollectionType(self):
        return self.collectionType


    def getName(self):
        return self.name


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
        result = []
        for elem in self.collection.nodes():
            if (attribute, str(value)) in elem:
                result.append(elem)
        return result
