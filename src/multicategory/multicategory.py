from initialization_of_demo_databases.initialize_ecommerce import ECommerceMultiModelDatabase
from initialization_of_demo_databases.initialize_patent_data import PatentMultiModelDatabase
from multi_model_db.multi_model_db import MultiModelDB

ecommer_db = ECommerceMultiModelDatabase().get_multi_model_db()
patent_db = PatentMultiModelDatabase().get_multi_model_db()

predefined_multi_model_dbs = [
    ecommer_db, patent_db, MultiModelDB("Online market place multi-model database", [], []), MultiModelDB("Small Unibench multi-model database", [], []), MultiModelDB(
        "University multi-model database", [], []), MultiModelDB("Person multi-model database", [], []), MultiModelDB("Film multi-model database", [], [])
]


class MultiCategory():

    def __init__(self, initial_db):
        self.multi_model_databases = dict()
        for db in predefined_multi_model_dbs:
            self.multi_model_databases[db.get_name()] = db
        self.external_databases = dict()
        self.selected_multi_model_database = self.multi_model_databases[initial_db]

    def get_multi_model_db_names(self):
        return list(self.multi_model_databases.keys())

    def get_multi_model_db_names_for_dropdown(self):
        return [{'label': db, 'value': db} for db in self.multi_model_databases]

    def get_multi_model_databases(self):
        return self.multi_model_databases

    def get_external_databases(self):
        return self.external_databases

    def get_selected_multi_model_database(self):
        return self.selected_multi_model_database

    def get_multi_model_db(self, db_name):
        if db_name in self.multi_model_databases.keys():
            return self.multi_model_databases[db_name]

    def change_to_multi_model_db(self, db):
        if db in self.multi_model_databases.keys():
            self.select_multi_model_db = self.multi_model_databases[db]
        elif db in self.multi_model_databases.values():
            self.select_multi_model_db = db
