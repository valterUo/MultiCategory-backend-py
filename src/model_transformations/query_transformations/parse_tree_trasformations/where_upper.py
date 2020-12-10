from model_transformations.query_transformations.parse_tree_trasformations.bool_expr import BooleanExpression
from model_transformations.query_transformations.parse_tree_trasformations.where import Where


class WhereUpper:

    def __init__(self, raw_where, from_clause, cte=False, cte_name = ""):
        self.raw_where = raw_where
        self.where = None
        self.from_clause = from_clause
        self.cte = cte
        self.cte_name = cte_name

        if "BoolExpr" in self.raw_where.keys():
            self.where = BooleanExpression(
                self.raw_where["BoolExpr"], self.from_clause, self.cte, self.cte_name)
        elif "A_Expr" in self.raw_where.keys():
            self.where = Where(self.raw_where, self.from_clause, self.cte, self.cte_name)
        elif "NullTest" in self.raw_where.keys():
            self.where = Where(self.raw_where, self.from_clause, self.cte, self.cte_name)

    def transform_into_cypher(self):
        return self.where.transform_into_cypher()

    def get_where(self):
        return self.where
