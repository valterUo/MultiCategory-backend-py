from initialization_of_demo_databases.initialize_ecommerce import ECommerceMultiModelDatabase
from initialization_of_demo_databases.initialize_patent_data import PatentMultiModelDatabase

patent_db = PatentMultiModelDatabase()
print(patent_db.get_instance())
ecommerce_db = ECommerceMultiModelDatabase()
print(ecommerce_db.get_instance())

patent_db.run_model_category_join_examples()

