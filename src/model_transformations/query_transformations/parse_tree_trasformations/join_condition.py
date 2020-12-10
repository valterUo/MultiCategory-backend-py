from model_transformations.query_transformations.parse_tree_trasformations.column import Column

class JoinCondition:

    def __init__(self, raw_join_cond, left, right):
        self.raw_join_cond = raw_join_cond
        self.location = None
        self.left_alias = left
        self.right_alias = right
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
        res += self.left.transform_into_cypher() + " "
        res += self.operator + " "
        res += self.right.transform_into_cypher()
        return res

