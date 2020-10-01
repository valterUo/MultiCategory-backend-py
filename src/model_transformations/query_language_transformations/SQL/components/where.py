import re

class WHERE:

    def __init__(self, condition_string):
        self.condition_string = condition_string
        self.conjunctive_part, self.disjunctive_part = self.parse_where()

    def parse_where(self):
        conjunctive_part = re.split(r'and', self.condition_string)
        disjunctive_part = []
        for i in range(len(conjunctive_part)):
            res = re.split('or', conjunctive_part[i])
            if len(res) > 1:
                conjunctive_part[i] = res[0]
                disjunctive_part.append(res[1])
        for elem in disjunctive_part:
            elem = elem.strip()
        for elem in conjunctive_part:
            elem = elem.strip()
        return conjunctive_part, disjunctive_part
