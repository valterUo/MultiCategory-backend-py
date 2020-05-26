import networkx as nx
from multi_model_join.graph_join.gluing_functions import glue_graphs
from instance_category.objects.collection_object import CollectionObject

# Implementation of the amalgam construction in the category of graphs and graph relations
# We assume that morphism is a collection of pairs of nodes so that the first term comes from
# the gluing graph and the second term is either from graph1 or graph2

def join_graph_graph(collectionObject1, morphism, collectionObject2, gluing_graph):
    graph1 = collectionObject1.getCollection()
    graph2 = collectionObject2.getCollection()
    if nx.number_of_nodes(graph1) == 0:
        composition_graph = nx.DiGraph()
    elif nx.number_of_nodes(graph2) == 0:
        composition_graph = graph1
    else:
        composition_graph = graph1
        # The following operation is expensive and its cost could be reduced if we would have
        # more information about the morphism i.e. we would know exactly the pairs (node1, node2)
        # which are mapped to true values i.e. included in the relation.
        for node1 in graph1.nodes:
            for node2 in graph2.nodes:
                if morphism(node1, node2):
                    composition_graph = glue_graphs(composition_graph, node1, graph2, node2, gluing_graph)
    newCollectionObject = CollectionObject(collectionObject1.getName(
    ) + " + " + collectionObject2.getName(), "property graph", None, lambda graph : list(graph.nodes), None, composition_graph)
    return newCollectionObject


def join_graph_relational(collectionObject1, morphism, collectionObject2):
    return None