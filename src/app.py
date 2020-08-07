from initialization_of_demo_databases.initialize_patent_data import PatentMultiModelDatabase

db = PatentMultiModelDatabase()
print(db.get_instance())