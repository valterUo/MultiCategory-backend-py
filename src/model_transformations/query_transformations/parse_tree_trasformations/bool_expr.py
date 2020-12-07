class BooleanExpression:

    """
    Postgres source code:

    typedef enum BoolExprType
    {
        AND_EXPR, OR_EXPR, NOT_EXPR
    } BoolExprType;

    Which means that boolop 0 -> AND, boolop 1 -> OR and boolop 2 -> NOT

    """

    def __init__(self, raw_expr, cte=False):
        self.raw_expr = raw_expr
        self.sources = []
        self.cte = cte
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
                    elem["BoolExpr"], self.cte))
            elif "A_Expr" in elem.keys():
                self.sources.append(
                    BooleanExpression(elem["A_Expr"], self.cte))

    def transform_into_cypher(self):
        res = ""
        return res
