class Limit:

    def __init__(self, limit_clause, cte = False):
        self.limit_clause = limit_clause
        self.cte = cte
        self.location = self.limit_clause["A_Const"]["location"]
        self.limit_value = str(self.limit_clause["A_Const"]["val"]["Integer"]["ival"])

    def transform_into_cypher(self):
        if self.cte:
            return "[.." + self.limit_value + "]" + "\n"
        return "LIMIT " + self.limit_value + "\n"