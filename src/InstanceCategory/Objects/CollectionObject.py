from DataParsers.CSVParser import readToTable
import networkx as nx
from DataParsers.PropertyGraphParser import parseDirectedGraph
from DataParsers.XMLParser import parseXML

class CollectionObject:

    """ 
    – file: path to the files or a list of paths
    – fileformat: the format that the file follows i.e. csv, json, rdf
    – collectionType: relational, property graph, RDF graph, tree structure
    – name: name of the object
    – separator: if the file is csv, this field specifies the separator
    """

    def __init__(self, filePaths, fileformat, collectionType, name, schema = None, keyAttribute = None, separator = ";", edgeSchema = None, edgeKeyAttribute = None, fromKeyAttribute = None, toKeyAttribute = None):
        self.filePaths = filePaths
        self.fileformat = fileformat
        self.collectionType = collectionType
        self.name = name
        self.schema = schema
        if self.collectionType == "relational":
            if self.fileformat == "csv":
                self.collection = readToTable(self.filePaths, separator, self.schema, keyAttribute)
        elif self.collectionType == "property graph":
            if self.fileformat == "csv":
                self.collection = parseDirectedGraph(filePaths[0], filePaths[1], separator, separator, schema, edgeSchema, keyAttribute, edgeKeyAttribute, fromKeyAttribute, toKeyAttribute)
        elif self.collectionType == "XML":
            self.collection = parseXML(filePaths)
        # # elif self.collectionType == "RDF graph":
        # # elif self.collectionType == "JSON":
        