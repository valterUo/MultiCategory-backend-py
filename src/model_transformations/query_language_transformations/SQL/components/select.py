import re

class SELECT:

    def __init__(self, attributes_string):
        self.attributes_with_aliases = re.split(r',(?![^(]*\))', attributes_string)
        self.attributes = []
        for attribute_with_alias in self.attributes_with_aliases:
            attribute_with_alias = attribute_with_alias.strip()
            if ' as ' in attribute_with_alias:
                attribute_and_alias = re.split(r'[\s]+as[\s]+', attribute_with_alias)
                self.parse_table_name(attribute_and_alias)
            elif ' ' in attribute_with_alias:
                attribute_and_alias = re.split(r'\s+', attribute_with_alias)
                self.parse_table_name(attribute_and_alias)
            else:
                self.parse_table_name([attribute_with_alias, None])

    def get_attributes(self):
        return self.attributes

    def parse_table_name(self, attribute):
        if '.' in attribute[0]:
            table_attribute_alias = re.split(r'\.(?![^(]*\))', attribute[0])
            if len(table_attribute_alias) > 1:
                self.attributes.append((table_attribute_alias[0], table_attribute_alias[1], attribute[1]))
            else:
                self.attributes.append((None, table_attribute_alias[0], attribute[1]))
        else:
            self.attributes.append((None, attribute[0], attribute[1]))