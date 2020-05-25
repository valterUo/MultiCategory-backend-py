from multi_model_join.relational_join_errors import RelationalJoinError

def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z


def add_to_dict(s, key, x):
    s[key] = x
    return s


def diff(first, second):
        second = set(second)
        return [item for item in first if item not in second]


def image(func, collection):
    elems = []
    for elem in collection:
        elems.append(func(elem))
    return set(elems)

def collect_values_from_xml(xml_elem, attibute):
    result = []
    root_result = xml_elem.findall(attibute)
    for elem in root_result:
        result.append(elem.text)
    for child in xml_elem:
        result = result + collect_values_from_xml(child, attibute)
    return result

def appendToResult(resultRows, result, attribute):
    for row in resultRows:
        row[attribute] = result
    return resultRows