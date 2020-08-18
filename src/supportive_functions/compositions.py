def compose_list_of_dictionaries(list1, list2):
    new_list = list()
    for dict1 in list1:
        for dict2 in list2:
            composition_dict = compose_dictionaries(dict1, dict2)
            if len(composition_dict.keys()) != 0:
                new_list.append(composition_dict)
    if len(new_list) == 0:
        return [{}]
    return new_list

def compose_dictionaries(dict2, dict1):
    composition_dict = dict()
    for key in dict1.keys():
        try:
            composition_dict[key] = dict2[dict1[key]]
        except:
            continue
    return composition_dict

## When lambda functions are composed, certain assumptions are necessary.
## Here we assume that all the lambda functions map to lists. This behaviour might be not the best.

def compose_lambda_functions(lambda1, lambda2):
    def composition_function(x):
        result = []
        for y in lambda2(x):
            for z in lambda1(y):
                result.append(z)
        return result
    return composition_function

def merge_two_dicts(x, y):
      z = x.copy()
      z.update(y)
      return z