import re

class SELECT:

    def __init__(self, attributes_string, from_part, db):
        # print("SELECT class: ", attributes_string)
        # print()

        self.from_part = from_part
        self.db = db

        self.attributes_with_aliases = re.split(
            r',(?![^(]*\))', attributes_string)
        self.attributes = []
        self.keys = []
        self.subqueries = []
        for elem in self.attributes_with_aliases:
            if 'select' in elem:
                self.subqueries.append(elem)
                self.attributes_with_aliases.remove(elem)
        for attribute_with_alias in self.attributes_with_aliases:
            attribute_with_alias = attribute_with_alias.strip()
            if ' as ' in attribute_with_alias:
                attribute_and_alias = re.split(
                    r'[\s]+as[\s]+', attribute_with_alias)
                self.parse_table_name(attribute_and_alias)
            elif ' ' in attribute_with_alias and '(' not in attribute_with_alias and ')' not in attribute_with_alias:
                attribute_and_alias = re.split(r'\s+', attribute_with_alias)
                self.parse_table_name(attribute_and_alias)
            else:
                self.parse_table_name([attribute_with_alias, None])
        print("Attributes: ", self.attributes)

    def get_attributes(self):
        return self.attributes

    def get_keys(self):
        return self.keys

    def parse_table_name(self, attribute):
        property, value, alias = None, None, None

        if attribute[1] != None:
            alias = attribute[1].replace('"', "").replace('.','_').strip()
            self.keys.append(alias)
        else:
            alias = attribute[0]
            if "_" in alias:
                alias = alias.split("_")[1]
            elif '.' in alias:
                alias = alias.split(".")[1]

        if '.' in attribute[0]:
            table_attribute_alias = re.split(r'\.(?![^(]*\))', attribute[0])
            if len(table_attribute_alias) > 1:
                value = table_attribute_alias[1]
                property = table_attribute_alias[0]
                if 'extract' in value:
                    value = self.map_postgres_extract_to_cypher(value)
                if '||' in value:
                    value = value.replace("||", "+")
            else:
                value = table_attribute_alias[0]
                if 'extract' in value:
                    value = self.map_postgres_extract_to_cypher(value)
                if '||' in value:
                    value = value.replace("||", "+")
        else:
            value = attribute[0]
            if 'extract' in value:
                value = self.map_postgres_extract_to_cypher(value)
            if '||' in value:
                    value = value.replace("||", "+")

        if property == None:
            for table in self.from_part.get_tables():
                    attributes = self.db.get_attributes_for_table(table[0])
                    for attr in attributes:
                        if attr.strip() in value.strip():
                            value = value.replace(attr, table[0] + "." + attr)
        self.attributes.append((property, value, alias))

    def map_postgres_extract_to_cypher(self, function_string):
        elements2 = []
        elements = function_string.replace(")", "").split("(")
        for elem in elements:
            elements2 += elem.split(" ")
        object_from = None
        source = None
        for i, elem in enumerate(elements2):
            if elem.strip() == "extract":
                source = elements2[i+1]
            if elem.strip() == "from":
                object_from = elements2[i+1]

        return "datetime(" + object_from + ")." + source
        
