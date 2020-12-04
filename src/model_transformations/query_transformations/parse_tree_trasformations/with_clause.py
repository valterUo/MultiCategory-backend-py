from model_transformations.query_transformations.parse_tree_trasformations.cte import CommonTableExpr


class WithClause:

    def __init__(self, with_clause):
        self.with_clause = with_clause["WithClause"]
        self.recursive = with_clause["WithClause"]["recursive"]
        self.location = with_clause["WithClause"]["location"]
        self.ctes = []
        raw_ctes = with_clause["WithClause"]["ctes"]
        for elem in raw_ctes:
            cte = elem["CommonTableExpr"]
            self.ctes.append(CommonTableExpr(cte))

    def transform_into_cypher(self):
        res = ""
        for cte in self.ctes:
            res += cte.transform_into_cypher() + "\n"
        return res