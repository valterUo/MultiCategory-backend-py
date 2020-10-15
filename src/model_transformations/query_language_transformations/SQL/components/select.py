import re

class SELECT:

    def __init__(self, attributes_string):
        self.attributes_with_aliases = re.split(
            r',(?![^(]*\))', attributes_string)
        self.attributes = []
        self.keys = []
        print(self.attributes_with_aliases)
        for attribute_with_alias in self.attributes_with_aliases:
            attribute_with_alias = attribute_with_alias.strip()
            if ' as ' in attribute_with_alias:
                attribute_and_alias = re.split(
                    r'[\s]+as[\s]+', attribute_with_alias)
                self.parse_table_name(attribute_and_alias)
            elif ' ' in attribute_with_alias:
                attribute_and_alias = re.split(r'\s+', attribute_with_alias)
                self.parse_table_name(attribute_and_alias)
            else:
                self.parse_table_name([attribute_with_alias, None])
        #print(self.attributes)

    def get_attributes(self):
        return self.attributes

    def get_keys(self):
        return self.keys

    def parse_table_name(self, attribute):
        alias = None
        if attribute[1] != None:
            alias = attribute[1].replace('"', "").replace('.','_').strip()
            self.keys.append(alias)

        if '.' in attribute[0]:
            table_attribute_alias = re.split(r'\.(?![^(]*\))', attribute[0])
            value = table_attribute_alias[1]
            if 'extract' in value:
                value = self.map_postgres_extract_to_cypher(value)
            if len(table_attribute_alias) > 1:
                self.attributes.append((table_attribute_alias[0], value, alias))
            else:
                value = table_attribute_alias[0]
                if 'extract' in value:
                    value = self.map_postgres_extract_to_cypher(value)
                self.attributes.append((None, value, alias))
        else:
            value = attribute[0]
            if 'extract' in value:
                value = self.map_postgres_extract_to_cypher(value)
            self.attributes.append((None, value, alias))
        print(self.attributes)

    def map_postgres_extract_to_cypher(self, function_string):
        elements2 = []
        elements = function_string.replace(")", "").split("(")
        for elem in elements:
            elements2 += elem.split(" ")
        print(elements2)
        object_from = None
        source = None
        for i, elem in enumerate(elements2):
            if elem.strip() == "extract":
                source = elements2[i+1]
            if elem.strip() == "from":
                object_from = elements2[i+1]

        return "datetime(" + object_from + ")." + source
        
