import re

class FROM:

    def __init__(self, join_type, table1, table2, condition):
        self.join_type = join_type # INNER, OUTER, FULL, etc.
        self.table1 = table1
        self.table2 = table2
        self.condition = condition

    def get_join_type(self):
        return self.join_type

    def get_table1(self):
        return self.table1

    def get_table2(self):
        return self.table2

    def get_condition(self):
        return self.condition