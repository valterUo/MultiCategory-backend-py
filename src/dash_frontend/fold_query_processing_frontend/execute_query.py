from multi_model_query_processing.fold import Fold

def execute_query(name, query_params):
    block = query_params[0]
    query_block = Fold(name, block["domain"], block["lambda_input"], block["return_attributes"], block["target_model"])
    i = 1
    for block in query_params[1:]:
        query_block = Fold(name + "_block_" + str(i), query_block.get_result_name(), block["lambda_input"], block["return_attributes"], block["target_model"])
        i+=1
    return query_block