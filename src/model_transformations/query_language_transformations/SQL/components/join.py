import re


class JOIN:

    def __init__(self, join_type, join_string, from_part):
        self.join_type = join_type  # INNER, OUTER, FULL, etc.
        self.join_string = join_string.strip()
        self.from_part = from_part
        self.table1, self.table2, self.condition, self.join_conditions = None, None, None, []
        self.parse_join()
        self.filtering_conditions = []

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
        return self.filtering_conditions

    # person_message_score pms on (pti.personid = pms.personid)
    def parse_join(self):
        parse = re.split(r' on ', self.join_string)
        self.table2 = (re.split(r' ', parse[0]))
        #print(self.table2)
        if self.from_part.get_table_from_alias(self.table2[1]) == None:
            self.from_part.add_table(self.table2)
        condition_without_paranthesis = re.sub(r'\(|\)', "", parse[1])
        #print(condition_without_paranthesis)
        parsed_condition = re.search(
            r'(.+)\.(.+)(=)(.+)\.(.+)', condition_without_paranthesis).groups()
        #print(parsed_condition)
        self.condition = ((parsed_condition[0], parsed_condition[1]),
                          parsed_condition[2], (parsed_condition[3], parsed_condition[4]))
        self.join_conditions.append(self.condition)
        if parsed_condition[0] != self.table2[1]:
            self.table1 = (self.from_part.get_table_from_alias(
                parsed_condition[0]), parsed_condition[0])
        else:
            self.table1 = (self.from_part.get_table_from_alias(
                parsed_condition[1]), parsed_condition[1])
        #print(self.table1)
