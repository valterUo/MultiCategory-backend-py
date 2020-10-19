import re


class FROM:

    def __init__(self, tables_string):
        print("FROM class: ", tables_string)
        print()
        self.tables_with_alias = re.split(r',', tables_string)
        self.tables = []
        for table_with_alias in self.tables_with_alias:
            table_with_alias = table_with_alias.strip()
            if 'as' in table_with_alias:
                self.tables.append(re.split(r'as', table_with_alias))
            elif ' ' in table_with_alias:
                self.tables.append(re.split(r'\s', table_with_alias))
            else:
                self.tables.append([table_with_alias, None])
        print("Tables: ", self.tables)

    def get_tables(self):
        return self.tables

    def add_table(self, table):
        self.tables.append(table)

    def get_table_from_alias(self, alias_name):
        for table in self.tables:
            #print(table)
            if table[1] == alias_name:
                return table[0]
        return alias_name
