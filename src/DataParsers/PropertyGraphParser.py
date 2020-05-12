import networkx as nx
from DataParsers.CSVParser import readNodesAndEdges
import matplotlib.pyplot as plt


def parseDirectedGraph(fileDictonaries):
    DG = nx.DiGraph()
    edges = readNodesAndEdges(fileDictonaries)
    for e in edges:
        DG.add_edge(e[0], e[1], object=e[2])
    return DG


def drawGraph(graph):
    nx.draw(graph, with_labels=True)
