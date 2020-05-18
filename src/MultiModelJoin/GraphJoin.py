import networkx as nx
from InstanceCategory.Objects.CollectionObject import CollectionObject


def join_graph_relational(collectionObject1, morphism, collectionObject2):
    return None

# Implementation of the amalgam construction in the category of graphs and graph relations
# We assume that morphism is a collection of pairs of nodes so that the first term comes from
# the gluing graph and the second term is either from graph1 or graph2
def join_graph_graph(collectionObject1, morphism, collectionObject2, gluing_graph):
    graph1 = collectionObject1.getCollection()
    graph2 = collectionObject2.getCollection()
    composition_graph = nx.compose(graph1, graph2)
    for edge in list(gluing_graph.edges):
        source, target = None, None
        for pair in morphism:
            if pair[0] == edge[0]:
                source = pair[1]
            if pair[0] == edge[1]:
                target = pair[1]
            if source != None and target != None:
                composition_graph.add_edge(source, target)
                source, target = None, None
    newCollectionObject = CollectionObject(collectionObject1.getName(
    ) + " + " + collectionObject2.getName(), "property graph", None, composition_graph)
    return newCollectionObject