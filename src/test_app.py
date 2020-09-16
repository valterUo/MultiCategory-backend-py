from initialization_of_demo_databases.initialize_ecommerce import ECommerceMultiModelDatabase
from initialization_of_demo_databases.initialize_patent_data import PatentMultiModelDatabase
from multi_model_join.model_category_join import ModelCategoryJoin

ecommerce = ECommerceMultiModelDatabase()

db1 = ecommerce.get_multi_model_db().get_objects()["customer"].get_model_category()
db2 = ecommerce.get_multi_model_db().get_objects()["location"].get_model_category()
mor1 = ecommerce.get_multi_model_db().get_morphisms()["customer_to_location_morphism"].get_model_relationship()

join = ModelCategoryJoin(db1, mor1, db2, True)

print(join.get_result().get_objects())
print(join.get_left_leg_model_relationship())
print(join.get_right_leg_model_relationship())