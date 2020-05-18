from InstanceCategory.Objects.CollectionObject import CollectionObject
from MultiModelJoin.HelpFunctions import merge_two_dicts


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
