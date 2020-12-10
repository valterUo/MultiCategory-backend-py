ctenames_to_column_names = dict()
column_names_to_cte_names = dict()
cte_names_to_iterator_variables = dict()
iterator_variables = ['x', 'y', 'z', 'k', 't', 'r', 's', 'p', 'h', 'q']

def ctenames_to_column_names_mapping(ctename):
    return ctenames_to_column_names[ctename]


def column_names_to_cte_names_mapping(column_name):
    return column_names_to_cte_names[column_name]


def set_column_names_for_cte(cte, columns):
    global ctenames_to_column_names
    if cte in ctenames_to_column_names.keys():
        ctenames_to_column_names[cte] += columns
    else:
        ctenames_to_column_names[cte] = columns


def set_cte_for_column_name(column, cte):
    global column_names_to_cte_names
    column_names_to_cte_names[column] = cte

def set_iterator_variable_to_cte(cte):
    global cte_names_to_iterator_variables
    i = 0
    while True:
        if cte not in cte_names_to_iterator_variables.keys():
            iterator = iterator_variables[i]
            if iterator not in cte_names_to_iterator_variables.values():
                cte_names_to_iterator_variables[cte] = iterator
                break
            i+=1
        else:
            break

def get_iterator_from_cte_column(column):
    return cte_names_to_iterator_variables[column_names_to_cte_names[column]]

def get_iterator_from_cte_name(name):
    return cte_names_to_iterator_variables[name]
