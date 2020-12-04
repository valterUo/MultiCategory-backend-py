from model_transformations.query_transformations.parse_tree_trasformations.select_stmt import SelectStmt


class SelectStmtCte:

    def __init__(self, select_stmt):
        self.select_stmt = select_stmt
        self.larg = SelectStmt(self.select_stmt["larg"]["SelectStmt"])
        self.rarg = SelectStmt(self.select_stmt["rarg"]["SelectStmt"])

    def transform_into_cypher(self):
        res = ""
        res += self.larg.transform_into_cypher()
        res += self.rarg.transform_into_cypher()
        print("cte: ", res)
        return res

