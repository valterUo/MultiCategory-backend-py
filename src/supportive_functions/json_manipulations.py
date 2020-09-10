import json
from supportive_functions.xml_to_dict import XmlDictConfig, XmlListConfig
from shelve import DbfilenameShelf

def decode_to_json(old_dict):
    new_dict = dict()
    for key in old_dict:
        try:
            new_dict[key] = old_dict[key].decode("utf-8")
        except:
            new_dict[key] = old_dict[key]
    return json.dumps(new_dict, indent=2)

def decode_shelve_to_json(previous_key, shelve_dict):
    new_dict = dict()
    if type(shelve_dict) == dict or type(shelve_dict) == XmlDictConfig or type(shelve_dict) == DbfilenameShelf:
        for key in shelve_dict:
            new_dict[key] = decode_shelve_to_json(key, shelve_dict[key])
    elif type(shelve_dict) == list or type(shelve_dict) == XmlListConfig:
        result = []
        for elem in shelve_dict:
            result.append(decode_shelve_to_json(None, elem))
        new_dict[previous_key] = result
    else:
        new_dict[previous_key] = shelve_dict
    return new_dict