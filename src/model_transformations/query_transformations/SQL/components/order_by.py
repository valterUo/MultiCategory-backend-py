import re


class ORDERBY:

    def __init__(self, attributes_string):
        self.attributes = re.split(r',', attributes_string)
        res = []
        for attr in self.attributes:
            res.append(attr)
        self.attributes = res

    def get_attributes(self):
        return self.attributes

    def get_order_by_cypher(self):
        return "ORDER BY " + ",".join(self.attributes)
