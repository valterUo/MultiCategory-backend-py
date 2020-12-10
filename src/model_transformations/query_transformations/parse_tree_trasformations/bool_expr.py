from model_transformations.query_transformations.parse_tree_trasformations.where import Where


class BooleanExpression:

    """
    Postgres source code:

    typedef enum BoolExprType
    {
        AND_EXPR, OR_EXPR, NOT_EXPR
    } BoolExprType;

    Which means that boolop 0 -> AND, boolop 1 -> OR and boolop 2 -> NOT

    """

    def __init__(self, raw_expr, from_clause, cte=False, cte_name = ""):
        self.raw_expr = raw_expr
        self.sources = []
        self.from_clause = from_clause
        self.cte = cte
        self.cte_name = cte_name
        self.boolop = self.raw_expr["boolop"]
        self.mapped_boolop = None

        if self.boolop == 0:
            self.mapped_boolop = "AND"
        elif self.boolop == 1:
            self.mapped_boolop = "OR"
        elif self.boolop == 2:
            self.mapped_boolop = "NOT"

        for elem in self.raw_expr["args"]:
            if "BoolExpr" in elem.keys():
                self.sources.append(BooleanExpression(
                    elem["BoolExpr"], self.from_clause, self.cte, self.cte_name))
            elif "A_Expr" in elem.keys():
                self.sources.append(
                    Where(elem, self.from_clause, self.cte, self.cte_name))
            elif "NullTest" in elem.keys():
                self.sources.append(Where(elem, self.from_clause, self.cte, self.cte_name))

    def transform_into_cypher(self, add_where = True):
        res = ""
        if add_where:
            res = "WHERE "
        for i, elem in enumerate(self.sources):
            if i == len(self.sources) - 1:
                res += elem.transform_into_cypher(False)
            else:
                res += elem.transform_into_cypher(False) + self.mapped_boolop + " "
        return res
