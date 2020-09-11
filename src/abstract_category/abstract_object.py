import uuid
"""
This class creates an abstract object of an abstract category or a model category. 
"""

class AbstractObject:

    def __init__(self, name, model, values = None):
        self.id = uuid.uuid4()
        self.name = name
        self.model = model
        self.values = values

    def get_name(self):
        return self.name

    def get_model(self):
        return self.model

    def get_values(self):
        return self.values

    def __str__(self):
        return self.name