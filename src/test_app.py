from initialization_of_demo_databases.initialize_ecommerce import ECommerceMultiModelDatabase
from initialization_of_demo_databases.initialize_patent_data import PatentMultiModelDatabase
from multi_model_join.model_category_join import ModelCategoryJoin
from multi_model_query_processing.fold import Fold

ecommerce = ECommerceMultiModelDatabase()

db1 = ecommerce.get_multi_model_db().get_objects()["customer"]
db2 = ecommerce.get_multi_model_db().get_objects()["location"]
# mor1 = ecommerce.get_multi_model_db().get_morphisms()["customer_to_location_morphism"].get_model_relationship()

# join = ModelCategoryJoin(db1, mor1, db2, True)

# print(join.get_result().get_objects())
# print(join.get_left_leg_model_relationship())
# print(join.get_right_leg_model_relationship())

fold_result = Fold("test_query_location", db2, "lambda x : x['location_id'] == 10", ['location_id', 'address', 'country'], "relational")

print(fold_result.get_result().get_length())

fold_result = Fold("test_query_customer", db1, "lambda x : x", 
{"vertex_object_attributes": ['customer_id', 'name', 'country'], "edge_object_attributes": []}, 
"graph")

print(fold_result.get_result().get_length())

## Pattern: (n)-[r]->(m)

