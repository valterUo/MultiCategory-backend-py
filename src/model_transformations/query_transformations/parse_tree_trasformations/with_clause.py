from model_transformations.query_transformations.parse_tree_trasformations.cte import CommonTableExpr


class WithClause:

    def __init__(self, with_clause):
        self.with_clause = with_clause
        self.ctes = []
        for i, elem in enumerate(self.with_clause["ctes"]):
            cte = elem["CommonTableExpr"]
            self.ctes.append(CommonTableExpr(cte, i))

    def transform_into_cypher(self):
        res = ""
        for cte in self.ctes:
            res += cte.transform_into_cypher() + "\n"
        return res
