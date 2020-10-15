import re


class FROM:

    def __init__(self, tables_string):
        self.tables_with_alias = re.split(r',', tables_string)
        self.tables = []
        for table_with_alias in self.tables_with_alias:
            table_with_alias = table_with_alias.strip()
            if 'as' in table_with_alias:
                self.tables.append(re.split(r'as', table_with_alias))
            elif ' ' in table_with_alias:
                self.tables.append(re.split(r'\s', table_with_alias))
            else:
                alias = ""
                if "_" in table_with_alias:
                    res = table_with_alias.split("_")
                    alias = res[0][:1] + res[1][:1]
                elif "." in table_with_alias:
                    res = table_with_alias.split(".")
                    alias = res[0][:1] + res[1][:1]
                else:
                    alias = table_with_alias[:2]
                self.tables.append([table_with_alias, alias])

    def get_tables(self):
        return self.tables

    def add_table(self, table):
        self.tables.append(table)

    def get_table_from_alias(self, alias_name):
        for table in self.tables:
            print(table)
            if table[1] == alias_name:
                return table[0]
