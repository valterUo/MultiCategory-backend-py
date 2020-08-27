from supportive_functions.compositions import merge_two_dicts
from supportive_functions.xml_to_dict import XmlListConfig, XmlDictConfig

## Row is already like a dictionary but because it is mutable and iterating over the rows changes this pointer
## this function solves the problem by creating a simple copy of the row.
def row_to_dictionary(row):
    dict_row = dict()
    attributes = row.table.colnames
    for key in attributes:
        dict_row[key] = row[key]
    return dict_row

## This function finds all the values from tree structure that have the key assigned with them
def find_values_from_tree(tree_dict, key):
    result = []
    #print("Current tree: ", str(tree_dict))
    if key in tree_dict.keys():
        if type(tree_dict[key]) == dict:
            result = result + list(tree_dict[key].values())
        elif type(tree_dict[key]) == list:
            result = result + tree_dict[key]
        else:
            result.append(tree_dict[key])
    for k in tree_dict.keys():
        if type(tree_dict[k]) == dict or type(tree_dict[k]) == XmlDictConfig:
            result = result + find_values_from_tree(tree_dict[k], key)
        elif type(tree_dict[k]) == list or type(tree_dict[k]) == XmlListConfig:
            for elem in tree_dict[k]:
                if type(elem) == dict or type(elem) == XmlDictConfig:
                    result = result + find_values_from_tree(elem, key)
    return result