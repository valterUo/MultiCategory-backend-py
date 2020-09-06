from decimal import Decimal


def formulate_set_string(value_dict):
    set_string = "SET a."
    i = 0
    attributes = value_dict.keys()
    for prop in attributes:
        if i == len(attributes) - 1:
            set_string = set_string + prop + " =$" + prop + " RETURN a"
        else:
            set_string = set_string + prop + " =$" + prop + ", a."
        i += 1
    return set_string


def fix_dictionary(value_dict):
    change_values = dict()
    for value in value_dict.values():
        if type(value) == memoryview:
            key = list(value_dict.keys())[
                list(value_dict.values()).index(value)]
            change_values[key] = None
        elif type(value) == Decimal:
            key = list(value_dict.keys())[
                list(value_dict.values()).index(value)]
            change_values[key] = float(value)
    for key in change_values:
        if change_values[key] == None:
            del value_dict[key]
        else:
            value_dict[key] = change_values[key]
    return value_dict
