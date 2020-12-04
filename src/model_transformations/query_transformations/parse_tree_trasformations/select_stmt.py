from model_transformations.query_transformations.parse_tree_trasformations.from_clause_transformation import FromClause
from model_transformations.query_transformations.parse_tree_trasformations.target import Target
import json

class SelectStmt:

    def __init__(self, select_stmt):
        #print(json.dumps(select_stmt, indent=2))
        self.select_stmt = select_stmt
        self.from_clause = None
        self.target = None
        self.where_clause = None
        self.with_clause = None
        self.sort_clause = None
        self.limit = None
        self.rarg = None
        self.larg = None

        if "larg" in self.select_stmt.keys() or "rarg" in self.select_stmt.keys():
            self.larg = SelectStmt(self.select_stmt["larg"]["SelectStmt"])
            self.rarg = SelectStmt(self.select_stmt["rarg"]["SelectStmt"])
        else:

            for clause in self.select_stmt:
                if clause == "fromClause":
                    self.from_clause = FromClause(self.select_stmt[clause])
                elif clause == "targetList":
                    self.target = Target(self.select_stmt[clause], self.from_clause)
                elif clause == "whereClause":
                    pass
                elif clause == "sortClause":
                    pass
                elif clause == "limitCount":
                    pass

    def transform_into_cypher(self):
        res = ""
        if self.larg and self.rarg:
            res += self.rarg.transform_into_cypher()
            res += self.larg.transform_into_cypher()
        else:
            res += self.from_clause.transform_into_cypher()
            res += self.target.transform_into_cypher()
        return res

