# This file contains an example of a graph amalgram construction.
# This code demonstrates a simple example of an usage of the amalgam.
# The more applied scenario is implemented in graph join.
# In practice we consider H as a common subgraph of G1 and G2 and form the union of G1 and G2 
# in such way that we paste together the two graphs along H.

import networkx as nx
import matplotlib.pyplot as plt

G1 = nx.Graph()
G1.add_edges_from([("x1", "x4"), ("x4", "x2"), ("x2", "x3")])
G2 = nx.Graph()
G2.add_edges_from([("y1", "y2"), ("y2", "y4"), ("y4", "y3")])
H = nx.Graph()
H.add_edges_from([("z2", "z4")])
H.add_node("z1")

def m1(x):
    if x == "z1":
        return "x3"
    elif x == "z2":
        return "x2"
    elif x == "z4":
        return "x4"

def m2(x):
    if x == "z1":
        return "y3"
    elif x == "z2":
        return "y2"
    elif x == "z4":
        return "y4"

def diff(first, second):
        second = set(second)
        return set([item for item in first if item not in second])

def image(func, graph):
    elems = []
    for elem in graph:
        elems.append(func(elem))
    return elems

def amalgam(collectionObject1, collectionObject2, H, m1, m2):
    amalgam = nx.Graph()
    V = list(H.nodes())
    for node in V:
        print(node)
    V1 = diff(collectionObject1.nodes(), image(m1, H.nodes()))
    for node in V1:
        print(node)
    V2 = diff(collectionObject2.nodes(), image(m2, H.nodes()))
    for node in V2:
        print(node)
    amalgam.add_nodes_from(V)
    amalgam.add_nodes_from(V1)
    amalgam.add_nodes_from(V2)
    acceptedEdges = []
    E1 = collectionObject1.edges()
    E2 = collectionObject2.edges()
    for edge in E1:
        if edge[0] in V1 and edge[1] in V2:
            acceptedEdges.append(edge)
    for edge in E2:
        if edge[0] in V1 and edge[1] in V2:
            acceptedEdges.append(edge)
    for z in V:
        for x in V1:
            if (x, m1(z)) in E1:
                acceptedEdges.append((x, z))
    for z in V:
        for x in V2:
            if (x, m2(z)) in E2:
                acceptedEdges.append((x, z))
    for z in V:
        for k in V:
            if (m1(z), m1(k)) in E1 or (m2(z), m2(k)) in E2:
                acceptedEdges.append((z, k))
    amalgam.add_edges_from(acceptedEdges)
    return amalgam


amalgamedGraph = amalgam(G1, G2, H, m1, m2)
print(amalgamedGraph.number_of_edges())
for edge in amalgamedGraph.edges():
    print(edge)
plt.subplot(121)
nx.draw(amalgamedGraph, with_labels=True, font_weight='bold')
plt.show()