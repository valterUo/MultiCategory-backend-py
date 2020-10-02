import re

class WHERE:

    def __init__(self, condition_string, primary_foreign_keys):
        self.condition_string = condition_string
        self.primary_foreign_keys = primary_foreign_keys
        self.conjunctive_part, self.disjunctive_part = self.parse_where()
        self.join_conditions = self.parse_join_conditions()

    def parse_where(self):
        conjunctive_part = re.split(r'[\s\n\r]+and[\s\n\r]+', self.condition_string)
        print()
        disjunctive_part = []
        for i in range(len(conjunctive_part)):
            res = re.split(r'[\s\n\r]+or[\s\n\r]+', conjunctive_part[i])
            if len(res) > 1:
                conjunctive_part[i] = res[0]
                disjunctive_part.append(res[1])
        self.parse_conditions(disjunctive_part)
        self.parse_conditions(conjunctive_part)
        return conjunctive_part, disjunctive_part

    def get_conjunctive_part(self):
        return self.conjunctive_part

    def get_disjunctive_part(self):
        return self.disjunctive_part

    def get_join_conditions(self):
        return self.join_conditions

    def parse_conditions(self, conds):
        for i in range(len(conds)):
            elem = conds[i].strip()
            if '=' in elem:
                res = re.split(r'=', elem)
                conds[i] = (res[0], '=', res[1])
            if '>' in elem:
                res = re.split(r'>', elem)
                conds[i] = (res[0], '>', res[1])
            if '<' in elem:
                res = re.split(r'<', elem)
                conds[i] = (res[0], '<', res[1])

    def parse_join_conditions(self):
        join_conditions = []
        for elem in self.conjunctive_part:
            if elem[1] == "=":
                left, right = False, False
                for key in self.primary_foreign_keys:
                    print(key, elem[0], elem[2])
                    if key in elem[0] or elem[0] in key:
                        left = True
                    if key in elem[2] or elem[2] in key:
                        right = True
                if left and right:
                    join_conditions.append(elem)
        return join_conditions