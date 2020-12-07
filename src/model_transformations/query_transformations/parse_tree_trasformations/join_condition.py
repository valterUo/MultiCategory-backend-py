from model_transformations.query_transformations.parse_tree_trasformations.column import Column

class JoinCondition:

    def __init__(self, raw_join_cond, cte = False):
        print(raw_join_cond)
        self.raw_join_cond = raw_join_cond
        self.cte = cte
        self.location = None
        self.left = None
        self.right = None
        self.operator = None
        if "A_Expr" in self.raw_join_cond.keys():
            self.operator = self.raw_join_cond["A_Expr"]["name"][0]["String"]["str"]

        if "A_Expr" in self.raw_join_cond.keys():
            self.location = self.raw_join_cond["A_Expr"]["location"]
            if "ColumnRef" in self.raw_join_cond["A_Expr"]["lexpr"]:
                self.left = Column(self.raw_join_cond["A_Expr"]["lexpr"]["ColumnRef"])

            if "ColumnRef" in self.raw_join_cond["A_Expr"]["rexpr"]:
                self.right = Column(self.raw_join_cond["A_Expr"]["rexpr"]["ColumnRef"])

    def transform_into_cypher(self):
        res = ""
        if self.cte:
            res += self.left.transform_into_cypher() + " "
            res += self.operator + " "
            res += self.right.transform_into_cypher() + "\n"
        return res

