import re

class GROUPBY:

    def __init__(self, attributes_string):
        self.attributes = re.split(r',', attributes_string)

    def get_attributes(self):
        return self.attributes