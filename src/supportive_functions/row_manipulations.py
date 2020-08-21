## Row is already like a dictionary but because it is mutable and iterating over the rows changes this pointer
## this function solves the problem by creating a simple copy of the row.

from supportive_functions.compositions import merge_two_dicts

def row_to_dictionary(row):
    dict_row = dict()
    attributes = row.table.colnames
    for key in attributes:
        dict_row[key] = row[key]
    return dict_row

## This function finds all the values from tree structure that have the key assigned with them
def find_values_from_tree(tree_dict, key):
    result = []
    if key in tree_dict.keys():
        if type(tree_dict[key]) == dict:
            result = result + list(tree_dict[key].values())
        elif type(tree_dict[key]) == list:
            result = result + tree_dict[key]
        else:
            result.append(tree_dict[key])
    for k in tree_dict:
        if type(tree_dict[k]) == dict:
            result = result + find_values_from_tree(tree_dict[k], key)
        elif type(tree_dict[k]) == list:
            for elem in tree_dict[key]:
                if type(elem) == dict:
                    result = result + find_values_from_tree(elem, key)
    return result


## This function does not work properly and it is not based on any working idea
def tree_to_row(tree_dict, schema):
    rows = [{}]
    if type(tree_dict) == dict:
        for key in tree_dict:
            if type(tree_dict[key]) == dict:
                sub_rows = tree_to_list_of_rows(tree_dict[key])
                expanded_rows = list()
                for row in rows:
                    for sub_row in sub_rows:
                        new_row = merge_two_dicts(row, sub_row)
                        expanded_rows.append(new_row)
                rows = expanded_rows
            elif type(tree_dict[key]) == list:
                for elem in tree_dict[key]:
                    sub_rows = tree_to_list_of_rows(elem)
                    expanded_rows = list()
                    for row in rows:
                        for sub_row in sub_rows:
                            new_row = merge_two_dicts(row, sub_row)
                            expanded_rows.append(new_row)
                    rows = expanded_rows
            else:
                for row in rows:
                    row[key] = tree_dict[key]
    elif type(tree_dict) == list:
        for elem in tree_dict:
            sub_rows = tree_to_list_of_rows(elem)
            expanded_rows = list()
            for row in rows:
                for sub_row in sub_rows:
                    new_row = merge_two_dicts(row, sub_row)
                    expanded_rows.append(new_row)
            rows = expanded_rows
    else:
        print("whats happening")
    return rows
