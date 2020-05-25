from instance_category.objects.collection_object import CollectionObject
from multi_model_join.help_functions import merge_two_dicts
from multi_model_join.xml_join import process_row_xml


def join_relational_relational_over_functional_morphism(collectionObject1, morphism, collectionObject2):
    newCollection = dict()
    for key in collectionObject1.getCollection():
                    source = collectionObject1.getCollection()[key]
                    target = morphism.getRelation(source)
                    newCollection[key] = merge_two_dicts(target, source)
    newCollectionObject = CollectionObject(collectionObject1.getName(
    ) + " + " + collectionObject2.getName(), "relational", collectionObject1.getDatatype() + " + " + collectionObject2.getDatatype(), lambda x: x, None, newCollection)
    return newCollectionObject


def join_relational_relational_over_nonfunctional_morphism(collectionObject1, morphism, collectionObject2):
    newCollection = dict()
    for key in collectionObject1.getCollection():
                    source = collectionObject1.getCollection()[key]
                    target = morphism.getRelation(source)
                    for target_key in target:
                        newCollection[key] = merge_two_dicts(
                            target[target_key], source)
    newCollectionObject = CollectionObject(collectionObject1.getName(
    ) + " + " + collectionObject2.getName(), "relational", collectionObject1.getDatatype() + " + " + collectionObject2.getDatatype(), lambda x: x, None, newCollection)
    return newCollectionObject


def join_relational_graph(collectionObject1, morphism, collectionObject2):
    table = collectionObject1.getCollection()
    new_table = None
    if type(table) == dict():
        new_table = dict()
        for row_key in table:
            row_from_graph = morphism(table[row_key])
            new_table[table_key] = merge_two_dicts(
                table[row_key], dict(row_from_graph))
    elif type(table) == list():
        new_table = []
        for row in table:
            row_from_graph = morphism(row)
            row = row + list(row_from_graph)
            new_table.append(row)
    return new_table


def join_relational_xml(collectionObject1, morphism, collectionObject2, pattern):
    table = collectionObject1.getCollection()
    resultCollection = None
    if type(table) == list:
        resultCollection = []
        for row in table:
            resultRows = process_row_xml(row, morphism, pattern)
            resultCollection = resultCollection + resultRows
    else:
        resultCollection = []
        for tableKey in table:
            row = table[tableKey]
            resultRows = process_row_xml(row, morphism, pattern)
            resultCollection = resultCollection + resultRows
    newCollectionObject = CollectionObject(collectionObject1.getName(
    ) + " + " + collectionObject2.getName(), "relational", collectionObject1.getDatatype() + " + " + collectionObject2.getDatatype(), lambda x: x, None, resultCollection)
    return newCollectionObject
