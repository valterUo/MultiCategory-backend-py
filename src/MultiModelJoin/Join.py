from InstanceCategory.Objects.CollectionObject import CollectionObject
import networkx as nx


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


def join_relational_relational_over_functional_morphism(collectionObject1, morphism, collectionObject2):
    newCollection = dict()
    for key in collectionObject1.getCollection():
                    source = collectionObject1.getCollection()[key]
                    target = morphism.getRelation()(source)
                    newCollection[key] = merge_two_dicts(target, source)
    newCollectionObject = CollectionObject(collectionObject1.getName(
    ) + " + " + collectionObject2.getName(), "relational", None, newCollection)
    return newCollectionObject


def join_relational_relational_over_nonfunctional_morphism(collectionObject1, morphism, collectionObject2):
    newCollection = dict()
    for key in collectionObject1.getCollection():
                    source = collectionObject1.getCollection()[key]
                    target = morphism.getRelation()(source)
                    for target_key in target:
                        newCollection[key] = merge_two_dicts(
                            target[target_key], source)
    newCollectionObject = CollectionObject(collectionObject1.getName(
    ) + " + " + collectionObject2.getName(), "relational", None, newCollection)
    return newCollectionObject


def join_relational_graph(collectionObject1, morphism, collectionObject2):
    return None


def join_graph_relational(collectionObject1, morphism, collectionObject2):
    return None


def join_graph_graph(collectionObject1, morphism, collectionObject2, pattern):
    return None

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

# Implementation of the amalgam construction in the category of graphs and graph relations
def rel_amalgam(graph1, graph2, H, rel1, rel2):
    return None

def join_relational_xml(collectionObject1, morphism, collectionObject2, pattern):
    tables = collectionObject1.getCollection()
    if type(tables) == list:
        resultCollection = []
        for row in tables:
            resultRow = dict()
            for attribute in pattern:
                if attribute in row.keys():
                    resultRow[attribute] = row[attribute]
                else:
                    xml_elem = morphism.getRelation(row)
                    result = collect_values_from_xml(xml_elem, attribute)
                    print(result)
                    if len(result) == 1:
                        resultRow[attribute] = result[0]
                    elif len(result) == 0:
                        resultRow[attribute] = "null"
    else:
        resultCollection = dict()
        for tableKey in tables:
            resultRow = dict()
            row = tables[tableKey]
            resultRow.update(row)
            xml_elem = morphism(row)
            for attribute in pattern:
                result = collect_values_from_xml(xml_elem, attribute)
                if len(result) == 1:
                    resultRow[attribute] = result[0]
                elif len(result) == 0:
                    resultRow[attribute] = "null"
    newCollectionObject = CollectionObject(collectionObject1.getName(
    ) + " + " + collectionObject2.getName(), "relational", None, resultCollection)
    return newCollectionObject


def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z


def add_to_dict(s, key, x):
    s[key] = x
    return s


def diff(first, second):
        second = set(second)
        return [item for item in first if item not in second]


def image(func, collection):
    elems = []
    for elem in collection:
        elems.append(func(elem))
    return set(elems)

def collect_values_from_xml(xml_elem, attibute):
    result = []
    root_result = xml_elem.findAll(attibute)
    for elem in root_result:
        result.append(elem.text())
    for child in xml_elem:
        result = result + collect_values_from_xml(child)
    return result
