import re

from model_transformations.query_transformations.SQL.independent_sql_parsing_tools import get_random_string


class JOIN:

    def __init__(self, join_type, join_string, from_part):
        self.join_type = join_type  # INNER, OUTER, FULL, etc.
        self.join_string = join_string.replace("\n", "").strip()
        self.from_part = from_part
        self.table1, self.table2, self.condition, self.join_conditions = None, None, None, []
        self.parse_join()
        self.from_part.add_table(self.table2)

    def get_join_type(self):
        return self.join_type

    def get_table1(self):
        return self.table1

    def get_table2(self):
        return self.table2

    def get_condition(self):
        return self.condition

    def get_join_conditions(self):
        return self.join_conditions

    def get_filtering_conditions(self):
        return []

    def parse_join(self):
        parse = re.split(r' on ', self.join_string)
        res_table2 = (re.split(r' ', parse[0]))
        if res_table2[1] == '':
            self.table2 = (res_table2[0], get_random_string(3))
        else:
            self.table2 = (res_table2[0], res_table2[1])
        condition_without_paranthesis = re.sub(r'\(|\)', "", parse[1])
        parsed_condition = re.search(
            r'(.+)\.(.+)(=)(.+)\.(.+)', condition_without_paranthesis).groups()
        self.condition = ((parsed_condition[0], parsed_condition[1]),
                          parsed_condition[2], (parsed_condition[3], parsed_condition[4]))
        self.join_conditions.append(self.condition)
        if parsed_condition[0] != self.table2[1]:
            self.table1 = [self.from_part.get_table_from_alias(
                parsed_condition[0]), parsed_condition[0]]
        else:
            self.table1 = [self.from_part.get_table_from_alias(
                parsed_condition[1]), parsed_condition[1]]