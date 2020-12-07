ctenames_to_column_names = dict()
column_names_to_cte_names = dict()


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
