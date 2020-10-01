import re

class SELECT:

    def __init__(self, attributes_string):
        self.attributes_with_aliases = re.split(",", attributes_string)
        self.attributes = []
        for attribute_with_alias in self.attributes_with_aliases:
            attribute_with_alias = attribute_with_alias.strip()
            if 'as' in attribute_with_alias:
                self.attributes.append(re.split(r'as', attribute_with_alias))
            elif ' ' in attribute_with_alias:
                self.attributes.append(re.split(r'\s', attribute_with_alias))
            else:
                self.attributes.append([attribute_with_alias, None])

    def get_attributes(self):
        return self.attributes