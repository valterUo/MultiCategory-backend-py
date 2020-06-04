import networkx as nx
import matplotlib.pyplot as plt
from data_parsers.csv_parser import readNodesAndEdges

def parseDirectedGraph(fileDictonaries):
    DG = nx.DiGraph()
    edges = readNodesAndEdges(fileDictonaries)
    for e in edges:
        DG.add_edge(e[0], e[1], object=e[2])
    return DG
