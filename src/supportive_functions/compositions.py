def compose_dictionaries(dict2, dict1):
    composition_dict = dict()
    for key in dict1.keys():
        try:
            composition_dict[key] = dict2[dict1[key]]
        except:
            continue

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