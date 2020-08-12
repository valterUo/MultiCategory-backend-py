class TableModelCategory:

    """
    TableModelCategory is a category with single object that is a sequence of attributes. 
    The sequence of attributes is always required. 
    The identity morphism is modelled only conceptually.
    """

    def __init__(self, name, attributes, primary_key = None):
        self.name = name
        self.attributes = attributes
        self.primary_key = primary_key

    def get_name(self):
        return self.name
    
    def get_attributes(self):
        return self.attributes

    def get_objects(self):
        return [self.attributes]

    def get_primary_key(self):
        return self.primary_key

    def __str__(self):
        return ", ".join(self.attributes)