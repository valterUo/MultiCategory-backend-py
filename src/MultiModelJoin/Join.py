from InstanceCategory.Objects.CollectionObject import CollectionObject
from MultiModelJoin.RelationalJoin import *
from MultiModelJoin.GraphJoin import *
from MultiModelJoin.XMLJoin import *
from MultiModelJoin.HelpFunctions import *
import networkx as nx
import copy


def join(collectionObject1, morphism, collectionObject2, pattern=None):
    type1 = collectionObject1.getCollectionType()
    type2 = collectionObject2.getCollectionType()
    if type1 == "relational":
        if type2 == "relational":
            if morphism.getFunctional():
                return join_relational_relational_over_functional_morphism(collectionObject1, morphism, collectionObject2)
            else:
                return join_relational_relational_over_nonfunctional_morphism(collectionObject1, morphism, collectionObject2)
        elif type2 == "property graph":
            return None
    elif type1 == "property graph":
        if type2 == "property graph":
            if pattern == None:
                return "Error"
            return join_graph_graph(collectionObject1, morphism, collectionObject2)


# Graph amalgam in the case that m1 and m2 are injective graph homomorphisms from H i.e. the amalgam construction
# in the category of graphs and graph homomorphisms
def amalgam(collectionObject1, collectionObject2, H, m1, m2):
    amalgam = nx.Graph()
    V = list(H.nodes())
    V1 = diff(collectionObject1.getCollection().nodes(), image(m1, H.nodes()))
    V2 = diff(collectionObject2.getCollection().nodes(), image(m2, H.nodes()))
    amalgam.add_nodes_from(V, V1, V2)
    acceptedEdges = []
    E1 = collectionObject1.getCollection().edges()
    E2 = collectionObject2.getCollection().edges()
    for edge in E1:
        if edge[0] in set(V1) and edge[1] in set(V2):
            acceptedEdges.append(edge)
    for edge in E2:
        if edge[0] in set(V1) and edge[1] in set(V2):
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