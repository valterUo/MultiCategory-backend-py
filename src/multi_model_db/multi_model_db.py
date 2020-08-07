class MultiModelDB:

    def __init__(self, name, multi_model_db_instance, multi_model_db_schema = None):
        self.name = name
        self.multi_model_db_instance = multi_model_db_instance
        if multi_model_db_schema != None:
            self.multi_model_db_schema = multi_model_db_schema
        else:
            self.multi_model_db_schema = self.construct_multi_model_db_schema()

    def construct_multi_model_db_schema(self):
        return None

    def get_name(self):
        return self.name

    def get_multi_model_db_instance(self):
        return self.multi_model_db_instance

    def get_multi_model_db_schema(self):
        return self.multi_model_db_schema

    def __str__(self):
        return self.name