from model_transformations.query_transformations.parse_tree_trasformations.from_clause_transformation import FromClause
from model_transformations.query_transformations.parse_tree_trasformations.target import Target


class SelectStmt:

    def __init__(self, select_stmt):
        self.select_stmt = select_stmt
        self.from_clause = []
        self.target = None

        for clause in self.select_stmt:
            if clause == "fromClause":
                self.from_clause = FromClause(self.select_stmt[clause])
            elif clause == "targetList":
                self.target = Target(self.select_stmt[clause], self.from_clause)
            elif clause == "whereClause":
                pass

    def transform_into_cypher(self):
        res = ""
        res += self.from_clause.transform_into_cypher()
        res += self.target.transform_into_cypher()
        return res
