from shelve import DbfilenameShelf
import copy
from supportive_functions.xml_to_dict import XmlDictConfig, XmlListConfig

def select(dictionary, return_info, previous_key):
    selection = dict()
    if type(return_info) == list:
        if type(dictionary) == dict or type(dictionary) == XmlDictConfig or type(dictionary) == DbfilenameShelf:
            for key in dictionary:
                if key in return_info:
                    #print("Dictionary printed: ", dictionary[key])
                    selection[key] = copy.deepcopy(dictionary[key])
                subresult = select(dictionary[key], return_info, key)
                if len(subresult) > 0:
                    if "subresults" not in selection.keys():
                        selection["subresults"] = []
                    selection["subresults"].append(subresult)
        elif type(dictionary) == list or type(dictionary) == XmlListConfig:
            list_result = []
            for elem in dictionary:
                result = select(elem, return_info, previous_key)
                if len(result) > 0:
                    list_result.append(result)
            if len(list_result) > 0:
                selection[previous_key] = list_result
    else:
        new_return_info = []
        for value in return_info.values():
            new_return_info.append(value)
        return select(dictionary, new_return_info, previous_key)
    return selection

def select_from_tuple(tupl, return_info, target_model):
    selection = dict()
    obj = tupl[- 1]
    for key in obj:
        if type(return_info) == list:
            if key in return_info:
                selection[key] = obj[key]
        elif type(return_info) == dict:
            values = []
            for value in return_info.values():
                values = values + value
            if key in values:
                selection[key] = obj[key]
    if target_model == "graph":
        if len(tupl) == 2:
            return (tupl[0], selection)
        elif len(tupl) == 3:
            return (tupl[0], tupl[1], selection)
    else:
        return selection