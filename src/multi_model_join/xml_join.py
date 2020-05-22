from instance_category.objects.collection_object import CollectionObject
from multi_model_join.help_functions import appendToResult, collect_values_from_xml
import copy


def process_row_xml(row, morphism, pattern):
    resultRows = []
    initial_result = dict()
    resultRows.append(initial_result)
    for attribute in pattern:
        if attribute in row.keys():
            appendToResult(resultRows, row[attribute], attribute)
        else:
            xml_elems = morphism.getRelation(row)
            if len(xml_elems) == 0:
                appendToResult(resultRows, "null", attribute)
            else:
                new_resultRows = []
                result_from_xml = []
                for elem in xml_elems:
                    for result in collect_values_from_xml(elem, attribute):
                        result_from_xml.append(result)
                for j in range(len(resultRows)):
                    for elem in result_from_xml:
                        new_resultRows.append(copy.deepcopy(resultRows[j]))
                for i in range(len(result_from_xml)):
                        new_resultRows[i][attribute] = result_from_xml[i]
                resultRows = new_resultRows
    return resultRows


def join_xml_relational(collectionObject1, morphism, collectionObject2):
    return None
