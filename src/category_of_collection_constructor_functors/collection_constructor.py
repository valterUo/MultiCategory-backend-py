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

    def get_iterable_collection_of_objects(self):
        return self.collection.get_iterable_collection_of_objects()