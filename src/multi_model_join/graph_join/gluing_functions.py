import networkx as nx
from multi_model_join.graph_join.graph_join_error import GraphJoinError

def glue_graphs(graph1, node0, graph2, node1, gluing_pattern):
    composition_graph = graph1
    if node0 not in graph1:
        raise GraphJoinError(node0, "Node 1 not in the graph 1!") 
    if node1 not in graph2:
        raise GraphJoinError(node1, "Node 1 not in the graph 1!")
    if gluing_pattern.number_of_nodes() > 1:
        fst_pattern = replace_node(gluing_pattern, 0, node0)
        sn_pattern = replace_node(fst_pattern, 1, node1)
        composition_graph = nx.compose_all([graph1, graph2, sn_pattern])
    elif gluing_pattern.number_of_nodes() == 0:
        raise GraphJoinError(gluing_pattern, "Join pattern is empty graph!")
    elif gluing_pattern.number_of_nodes() == 1:
        composition_graph = overlay_on_single_node(composition_graph, node0, graph2, node1)
    return composition_graph

def replace_node(graph, old_node, new_node):
    predecessors_of_old_node = graph.predecessors(old_node)
    successors_of_old_node = graph.successors(old_node)
    graph.remove_node(old_node)
    graph.add_node(new_node)
    for node in predecessors_of_old_node:
        graph.add_edge(node, new_node)
    for node in successors_of_old_node:
        graph.add_edge(new_node, node)
    return graph

def overlay_on_single_node(graph1, node0, graph2, node1):
    new_node = frozenset({node0, node1})
    if len(new_node) == 1:
        new_node = list(new_node)[0]
    new_graph = replace_node(graph1, node0, new_node)
    new_graph2 = replace_node(graph2, node1, new_node)
    return nx.compose(new_graph, new_graph2)
