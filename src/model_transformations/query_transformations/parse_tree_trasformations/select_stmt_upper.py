#from model_transformations.query_transformations.parse_tree_trasformations.join import Join
from model_transformations.query_transformations.parse_tree_trasformations.select_stmt import SelectStmt
from model_transformations.query_transformations.parse_tree_trasformations.with_clause import WithClause


class SelectStmtUpper:

    def __init__(self, select_stmt):
        self.with_clause = None
        self.stmt = None
        self.stmt = SelectStmt(select_stmt)
        self.joins = []

        if "withClause" in select_stmt.keys():
            self.with_clause = WithClause(select_stmt["withClause"])

    def transform_into_cypher(self):
        res = ""
        res += self.with_clause.transform_into_cypher() + "\n"
        for elem in self.joins:
            res += elem.transform_into_cypher()
        res += self.stmt.transform_into_cypher()
        return res
