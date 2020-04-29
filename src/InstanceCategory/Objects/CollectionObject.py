from DataParsers.CSVParser import readToTable
import networkx as nx

class CollectionObject:

    """ 
    – file: path to the files or a list of paths
    – fileformat: the format that the file follows i.e. csv, json, rdf
    – collectionType: relational, property graph, RDF graph, tree structure
    – name: name of the object
    – separator: if the file is csv, this field specifies the separator
    """

    def __init__(self, filePaths, fileformat, collectionType, name, schema, keyAttribute, separator = ";"):
        self.filePaths = filePaths
        self.fileformat = fileformat
        self.collectionType = collectionType
        self.name = name
        self.schema = schema
        if self.collectionType == "relational":
            if self.fileformat == "csv":
                self.collection = readToTable(self.filePaths, separator, self.schema, keyAttribute)
        # elif self.collectionType == "property graph":
        #     if self.fileformat == "csv":

        # # elif self.collectionType == "RDF graph":
        # # elif self.collectionType == "JSON":
        # # elif self.collectionType == "XML":