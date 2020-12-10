from model_transformations.query_transformations.parse_tree_trasformations.join import Join
from model_transformations.query_transformations.parse_tree_trasformations.select_stmt import SelectStmt
from model_transformations.query_transformations.parse_tree_trasformations.with_clause import WithClause


class SelectStmtUpper:

    def __init__(self, select_stmt):
        self.with_clause = None
        self.joins = []

        if "withClause" in select_stmt.keys():
            self.with_clause = WithClause(select_stmt["withClause"]["WithClause"])
        
        if "fromClause" in select_stmt.keys():
            for elem in select_stmt["fromClause"]:
                if "JoinExpr" in elem.keys():
                    self.joins.append(Join(elem["JoinExpr"]))

        self.main_stmt = SelectStmt(select_stmt, name = "main", joins = self.joins, with_clause = self.with_clause)

    def transform_into_cypher(self):
        res = ""
        res += self.with_clause.transform_into_cypher() + "\n"
        for elem in self.joins:
            res += elem.transform_into_cypher()
        res += self.main_stmt.transform_into_cypher()
        return res
