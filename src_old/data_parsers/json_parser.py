import json
from json import JSONDecodeError

def parse_json(json_file):
    try:
        data_set = json.load(json_file)
    except JSONDecodeError:
        print("JSON Decoder Error. Trying read line by line.")
        try:
            data_set = []
            json_file.seek(0,0)  
            for json_line in json_file.readlines():
                parsed_line = json.loads(json_line)
                data_set.append(parsed_line)
        except Exception as e:
            print("JSON file is invalid: ", e)
    return data_set