import networkx as nx
from DataParsers.CSVParser import readNodesAndEdges
import matplotlib.pyplot as plt


def parseDirectedGraph(filePathNodes: str, filePathEdges: str, delimiterNodes: str, delimiterEdges: str, schemaNodes: [str], schemaEdges: [str],
                       keyAttributeNodes: str, keyAttributeEdges: str, fromKeyAttribute: str, toKeyAttribute: str):
    DG = nx.DiGraph()
    edges = readNodesAndEdges(filePathNodes, filePathEdges, delimiterNodes, delimiterEdges, schemaNodes,
                              schemaEdges, keyAttributeNodes, keyAttributeEdges, fromKeyAttribute, toKeyAttribute)
    for e in edges:
        DG.add_edge(e[0], e[1], object=e[2])
    return DG


def drawGraph(graph):
    nx.draw(graph, with_labels=True)
