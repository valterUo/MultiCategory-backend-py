import networkx as nx
import uuid
from supportive_functions.xml_to_dict import XmlListConfig, XmlDictConfig

def compose_list_of_dictionaries(list1, list2):
    new_list = list()
    for dict1 in list1:
        for dict2 in list2:
            composition_dict = compose_dictionaries(dict1, dict2)
            if len(composition_dict.keys()) != 0:
                new_list.append(composition_dict)
    if len(new_list) == 0:
        return [{}]
    return new_list

def compose_dictionaries(dict2, dict1):
    composition_dict = dict()
    for key in dict1.keys():
        try:
            composition_dict[key] = dict2[dict1[key]]
        except:
            continue
    return composition_dict

## When lambda functions are composed, certain assumptions are necessary.
## Here we assume that all the lambda functions map to lists. This behaviour might be not the best.

def compose_lambda_functions(lambda1, lambda2):
    def composition_function(x):
        result = []
        for y in lambda2(x):
            #print(y)
            for z in lambda1(y):
                #print(z)
                result.append(z)
        return result
    return composition_function

def merge_two_dicts(x, y):
    #print(x)
    z = x.copy()
    z.update(y)
    return z

## Graph union that works as vertex set G union vertex set H and edge set G union edge set H.
## I wonder the default graph union of networkx requires that G and H are disjoint.
## This union identifies nodes that have same id and combines the dictionaries together.

def graph_union(G, H):
    union_graph = nx.DiGraph()
    ## Processing nodes
    G_nodes_with_data = dict(G.nodes.data())
    H_nodes_with_data = dict(H.nodes.data())
    for key in G_nodes_with_data:
        if key in H_nodes_with_data.keys():
            new_dict = merge_two_dicts(G_nodes_with_data[key], H_nodes_with_data[key])
            union_graph.add_nodes_from([(key, new_dict)])
        else:
            union_graph.add_nodes_from([(key, G_nodes_with_data[key])])
    for key in H_nodes_with_data:
        if key not in G_nodes_with_data.keys():
            union_graph.add_nodes_from([(key, H_nodes_with_data[key])])
    ## Processing edges
    G_edges_with_data = nx.to_dict_of_dicts(G)
    H_edges_with_data = nx.to_dict_of_dicts(H)
    for G_key1 in G_edges_with_data:
        if G_key1 in H_edges_with_data.keys():
            for G_key2 in G_edges_with_data[G_key1]:
                if G_key2 in H_edges_with_data[G_key1]:
                    G_data = G_edges_with_data[G_key1][G_key2]
                    H_data = H_edges_with_data[G_key1][G_key2]
                    new_dict = merge_two_dicts(G_data, H_data)
                    union_graph.add_edges_from([(G_key1, G_key2, new_dict)])
                else:
                    G_data = G_edges_with_data[G_key1][G_key2]
                    union_graph.add_edges_from([(G_key1, G_key2, G_data)])
        else:
            for G_key2 in G_edges_with_data[G_key1]:
                G_data = G_edges_with_data[G_key1][G_key2]
                union_graph.add_edges_from([(G_key1, G_key2, G_data)])
    for H_key1 in H_edges_with_data:
        if H_key1 not in G_edges_with_data.keys():
            for H_key2 in H_edges_with_data[H_key1]:
                H_data = H_edges_with_data[H_key1][H_key2]
                union_graph.add_edges_from([(H_key1, H_key2, H_data)])
        else:
            for H_key2 in H_edges_with_data[H_key1]:
                if H_key2 not in G_edges_with_data[H_key1]:
                    H_data = H_edges_with_data[H_key1][H_key2]
                    union_graph.add_edges_from([(H_key1, H_key2, H_data)])
    return union_graph

def tree_to_nx_graph(tree, G, root_id):
    if type(tree) == dict or type(tree) == XmlDictConfig:
        for key in tree.keys():
            child_id = uuid.uuid4()
            G.add_nodes_from([(child_id, {"tag": key})])
            G.add_edge(root_id, child_id)
            tree_to_nx_graph(tree[key], G, child_id)
    elif type(tree) == list or type(tree) == XmlListConfig:
        for elem in tree:
            tree_to_nx_graph(elem, G, root_id)
    else:
        child_id = uuid.uuid4()
        G.add_node(child_id)
        G.nodes[child_id]["value"] = tree
        G.add_edge(root_id, child_id)


## Because every tree is also a graph, we can create the union of tree and graph similarly as the union of
## graph and graph
def graph_union_with_tree(graph, tree):
    union_graph = nx.DiGraph()
