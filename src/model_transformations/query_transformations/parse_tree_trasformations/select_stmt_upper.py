from model_transformations.query_transformations.parse_tree_trasformations.from_clause_transformation import FromClause
from model_transformations.query_transformations.parse_tree_trasformations.select_stmt import SelectStmt
from model_transformations.query_transformations.parse_tree_trasformations.select_stmt_cte import SelectStmtCte
from model_transformations.query_transformations.parse_tree_trasformations.with_clause import WithClause


class SelectStmtUpper:

    def __init__(self, select_stmt):
        self.with_clause = None
        self.stmt = None
        self.stmt = SelectStmt(select_stmt)
        if "withClause" in select_stmt.keys():
            self.with_clause = WithClause(select_stmt["withClause"])
            

    def transform_into_cypher(self):
        res = ""
        res += self.with_clause.transform_into_cypher() + "\n"
        res += self.stmt.transform_into_cypher()
        return res

