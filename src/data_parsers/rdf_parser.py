import rdflib

class RDFParser:
    
    def __init__(self, filePath):
        g = rdflib.Graph()
        self.rdf = g.parse(filePath)

    
    def printRDF(self):
        for subj, pred, obj in self.rdf:
            print(subj, pred, obj)

    def __str__(self):
        for subj, pred, obj in self.rdf:
                return subj + " " + pred + " " + obj