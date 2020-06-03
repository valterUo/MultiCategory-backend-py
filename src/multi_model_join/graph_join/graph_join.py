import networkx as nx
from multi_model_join.graph_join.gluing_functions import glue_graphs, replace_node
from instance_category.objects.collection_object import CollectionObject
from multi_model_join.help_functions import deep_copy_graph, merge_two_dicts
from multi_model_join.graph_join.graph_join_error import GraphRelationalJoinError

# Implementation of the amalgam construction in the category of graphs and graph relations
# We assume that morphism is a collection of pairs of nodes so that the first term comes from
# the gluing graph and the second term is either from graph1 or graph2

def join_graph_graph(collectionObject1, morphism, collectionObject2, gluing_graph):
    graph1 = collectionObject1.get_collection()
    graph2 = collectionObject2.get_collection()
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
                print(node1, node2)
                if morphism(node1, node2):
                    composition_graph = glue_graphs(composition_graph, node1, graph2, node2, gluing_graph)
    newCollectionObject = CollectionObject(collectionObject1.getName() 
    + " + " + collectionObject2.getName(), "property graph", None, lambda graph : list(graph.nodes), None, composition_graph)
    return newCollectionObject


def join_graph_relational(collectionObject1, morphism, collectionObject2):
    result = collectionObject1.get_collection()
    for graph_elem in collectionObject1.get_access_to_iterable():
        row = morphism.getRelation(graph_elem)
        if type(row) == dict:
            new_node = merge_two_dicts(row, dict(graph_elem))
            result = replace_node(result, graph_elem, frozenset(new_node.items()))
        elif type(row) == set or type(row) == list:
            row_name = collectionObject2.getName()
            graph_element = dict(graph_elem)
            graph_element[row_name] = frozenset(row)
            result = replace_node(result, graph_elem, frozenset(new_node.items()))
        else:
            raise GraphRelationalJoinError(row, "The row needs to be a dictionary.")
    newCollectionObject = CollectionObject(collectionObject1.getName() 
    + " + " + collectionObject2.getName(), "property graph", None, lambda graph : list(graph.nodes), None, result)
    return newCollectionObject