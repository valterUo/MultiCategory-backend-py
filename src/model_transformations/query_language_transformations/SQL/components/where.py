import re

class WHERE:

    def __init__(self, condition_string, primary_foreign_keys):
        self.condition_string = condition_string
        self.primary_foreign_keys = primary_foreign_keys
        self.join_type = "inner"
        self.conjunctive_part, self.disjunctive_part = self.parse_where()
        self.join_conditions = self.parse_join_conditions()
        self.filtering_conditions = [
            cond for cond in self.conjunctive_part if cond not in self.join_conditions]

    def get_conjunctive_part(self):
        return self.conjunctive_part

    def get_disjunctive_part(self):
        return self.disjunctive_part

    def get_join_conditions(self):
        return self.join_conditions

    def get_join_type(self):
        return self.join_type

    def get_filtering_conditions(self):
        return self.filtering_conditions

    def parse_where(self):
        conjunctive_part = re.split(
            r'[\s\n\r]+and[\s\n\r]+', self.condition_string)
        disjunctive_part = []
        for i in range(len(conjunctive_part)):
            res = re.split(r'[\s\n\r]+or[\s\n\r]+', conjunctive_part[i])
            if len(res) > 1:
                conjunctive_part[i] = res[0]
                disjunctive_part.append(res[1])
        self.parse_conditions(disjunctive_part)
        self.parse_conditions(conjunctive_part)
        return conjunctive_part, disjunctive_part

    def parse_conditions(self, conds):
        for i in range(len(conds)):
            elem = conds[i].strip()
            if '=' in elem:
                res = re.split(r'=', elem)
                conds[i] = self.construct_conds(res, '=')
            if '>' in elem:
                res = re.split(r'>', elem)
                conds[i] = self.construct_conds(res, '>')
            if '<' in elem:
                res = re.split(r'<', elem)
                conds[i] = self.construct_conds(res, '<')

    def parse_join_conditions(self):
        join_conditions = []
        for elem in self.conjunctive_part:
            if elem[1] == "=":
                left, right = False, False
                for key in self.primary_foreign_keys:
                    if type(elem[0]) == tuple:
                        if key.strip() == elem[0][1].strip():
                            left = True
                    if type(elem[2]) == tuple:
                        if key.strip() == elem[2][1].strip():
                            right = True
                    if type(elem[0]) == str:
                        if key.strip() == elem[0].strip():
                            left = True
                    if type(elem[2]) == str:
                        if key.strip() in elem[2].strip():
                            right = True
                if left and right:
                    join_conditions.append(elem)
        return join_conditions

    def construct_conds(self, res, operator):
        table_attr0, table_attr1 = None, None
        if '.' in res[0]:
            table_attr0 = re.split(r'\.', res[0])
        if '.' in res[1]:
            table_attr1 = re.split(r'\.', res[1])
        if table_attr0 != None and table_attr1 != None:
            return ((table_attr0[0], table_attr0[1]), operator, (table_attr1[0], table_attr1[1]))
        elif table_attr0 != None:
            return ((table_attr0[0], table_attr0[1]), operator, res[1])
        elif table_attr1 != None:
            return (res[0], operator, (table_attr1[0], table_attr1[1]))
        else:
            return (res[0], operator, res[1])
