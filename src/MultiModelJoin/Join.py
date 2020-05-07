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
    return newCollection


def join_relational_relational_over_nonfunctional_morphism(collectionObject1, morphism, collectionObject2):
    newCollection = dict()
    for key in collectionObject1.getCollection():
                    source = collectionObject1.getCollection()[key]
                    target = morphism.getRelation()(source)
                    for target_key in target:
                        newCollection[key] = merge_two_dicts(
                            target[target_key], source)
    return newCollection


def join_graph_graph(collectionObject1, morphism, collectionObject2, pattern):
    return None


def join_graph_relational():
    return None


def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z


def add_to_dict(s, key, x):
    s[key] = x
    return s
