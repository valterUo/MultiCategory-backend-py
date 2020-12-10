cte_table_data = dict()
iterator_variables = ['x', 'y', 'z', 'k', 't', 'r', 's', 'p', 'h', 'q']

def append_cte_table_data(cte_table_name, cte_table_alias, cte_column_names, cte_iterator_variable):
    global cte_table_data
    if cte_table_name not in cte_table_data.keys():
        cte_table_data[cte_table_name] = {"cte_column_names" : cte_column_names, "cte_table_alias": cte_table_alias, "cte_iterator_variable": cte_iterator_variable}

def get_cte_iterator_for_cte_name(name):
    return cte_table_data[name]["cte_iterator_variable"]

def get_cte_iterator_for_cte_table_alias(alias):
    for key in cte_table_data:
        if cte_table_data[key]["cte_table_alias"] == alias:
            return cte_table_data[key]["cte_iterator_variable"]

def get_cte_column_names_for_cte_name(name):
    return cte_table_data[name]["cte_column_names"]

def get_cte_iterator_for_cte_column_name(column):
    for key in cte_table_data:
        if column in cte_table_data[key]["cte_column_names"]:
            return cte_table_data[key]["cte_iterator_variable"]

def get_cte_table_name_for_cte_iterator(iterator):
    for key in cte_table_data:
        if cte_table_data[key]["cte_iterator_variable"] == iterator:
            return key

def is_cte(cte):
    return cte in cte_table_data.keys()

def set_iterator_variable_to_cte(cte):
    global cte_table_data
    i = 0
    if cte not in cte_table_data.keys():
        cte_table_data[cte] = dict()
        while True:
            iterator = iterator_variables[i]
            if iterator not in [iter["cte_iterator_variable"] for iter in cte_table_data.values() if "cte_iterator_variable" in iter.keys()]:
                cte_table_data[cte]["cte_iterator_variable"] = iterator
                break
            i+=1