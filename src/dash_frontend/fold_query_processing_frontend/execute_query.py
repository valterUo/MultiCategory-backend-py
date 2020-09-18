from multi_model_query_processing.fold import Fold
import uuid

def execute_query(query_params):
    block = query_params[0]
    name = uuid.uuid4()
    query_block = Fold(name, block["domain"], block["lambda_input"], block["return_attributes"], block["target_model"])
    for block in query_params[1:]:
        name = uuid.uuid4()
        query_block = Fold(name, query_block, block["lambda_input"], block["return_attributes"], block["target_model"])
    return query_block