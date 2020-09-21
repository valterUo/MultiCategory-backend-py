class CollectionConstructor:

    def __init__(self, name, model_category, collection):
        self.name = name
        self.model_category = model_category
        self.collection = collection

    def get_name(self):
        return self.name

    def get_model_category(self):
        return self.model_category

    def get_collection(self):
        return self.collection

    def get_model(self):
        return self.model_category.get_model()

    def get_model_category_as_nx_graph(self):
        return self.model_category.get_nx_graph()

    def get_iterable_collection_of_objects(self):
        return self.collection.get_iterable_collection_of_objects()

    def append_to_collection(self, new_data_point):
        self.collection.append_to_collection(new_data_point)

    def get_length(self):
        return self.collection.get_length()

    def get_attributes_from_model_category(self):
        return self.model_category.get_attributes()