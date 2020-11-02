import re

from model_transformations.query_language_transformations.SQL.independent_sql_parsing_tools import get_random_string


class FROM:

    def __init__(self, tables_string):
        # print("FROM class: ", tables_string)
        # print()

        self.tables_with_alias = re.split(r',', tables_string)
        self.tables = []
        self.cte_tables = dict()
        for table_with_alias in self.tables_with_alias:
            table_with_alias = table_with_alias.strip()
            if 'as' in table_with_alias:
                self.tables.append(re.split(r'as', table_with_alias))
            elif ' ' in table_with_alias:
                self.tables.append(re.split(r'\s', table_with_alias))
            else:
                print(table_with_alias)
                var = get_random_string(3)
                self.tables.append([table_with_alias, var])
        print("Tables: ", self.tables)

    def get_tables(self):
        return self.tables

    def add_cte_table_attribute(self, table, attribute):
        if table not in self.cte_tables.keys():
            self.cte_tables[table] = [attribute]
        else:
            self.cte_tables[table].append(attribute)

    def get_cte_attributes(self, table):
        if table in self.cte_tables.keys():
            return self.cte_tables[table]

    def get_cte_table_from_attribute(self, attribute):
        for key in self.cte_tables.keys():
            if attribute.strip() in self.cte_tables[key]:
                return key

    def add_table(self, table):
        self.tables.append(table)
        print("Tables: ", self.tables)

    def get_table_from_alias(self, alias_name):
        for table in self.tables:
            if table[1] == alias_name:
                return table[0]
        return alias_name

    def get_alias_from_table(self, table_name):
        for table in self.tables:
            if table[0] == table_name:
                return table[1]
        return table_name
