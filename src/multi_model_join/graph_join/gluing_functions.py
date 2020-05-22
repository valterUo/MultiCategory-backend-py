import networkx as nx
from multi_model_join.graph_join.join_error import JoinPatternError

def glue_graphs(graph1, node0, graph2, node1, gluing_pattern):
    copy_gluing_graph = gluing_pattern.copy()
    composition_graph = graph1
    if node0 not in graph1:
        raise JoinPatternError("Node 1 not in the graph 1!", "Node 1 not in the graph 1!") 
    if node1 not in graph2:
        raise JoinPatternError("Node 2 not in the graph 2!", "Node 1 not in the graph 1!")
    if gluing_pattern.number_of_nodes() > 1:
        fst_pattern = replace_node(copy_gluing_graph, 0, node0)
        sn_pattern = replace_node(fst_pattern, 1, node1)
        composition_graph = nx.compose_all([graph1, graph2, sn_pattern])
    elif gluing_pattern.number_of_nodes() == 0:
        raise JoinPatternError("Join pattern is empty graph!")
    elif gluing_pattern.number_of_nodes() == 1:
        composition_graph = overlay_on_single_node(composition_graph, node0, graph2, node1)
    return composition_graph

def replace_node(graph, old_node, new_node):
    new_graph = graph.copy()
    predecessors_of_old_node = new_graph.predecessors(old_node)
    successors_of_old_node = new_graph.successors(old_node)
    new_graph.remove_node(old_node)
    new_graph.add_node(new_node)
    for node in predecessors_of_old_node:
        new_graph.add_edge(node, new_node)
    for node in successors_of_old_node:
        new_graph.add_edge(new_node, node)
    return new_graph

def overlay_on_single_node(graph1, node0, graph2, node1):
    # print("Node 1:", node0)
    # print("Node 2:", node1)
    new_node = frozenset({node0, node1})
    if len(new_node) == 1:
        new_node = list(new_node)[0]
    new_graph = replace_node(graph1, node0, new_node)
    new_graph2 = replace_node(graph2, node1, new_node)
    return nx.compose(new_graph, new_graph2)
