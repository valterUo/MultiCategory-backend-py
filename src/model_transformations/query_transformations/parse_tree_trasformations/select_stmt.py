from model_transformations.query_transformations.parse_tree_trasformations.from_clause import FromClause
from model_transformations.query_transformations.parse_tree_trasformations.limit import Limit
from model_transformations.query_transformations.parse_tree_trasformations.recursive import Recursive
from model_transformations.query_transformations.parse_tree_trasformations.sort import Sort
from model_transformations.query_transformations.parse_tree_trasformations.target import Target
from model_transformations.query_transformations.parse_tree_trasformations.where_upper import WhereUpper


class SelectStmt:

    def __init__(self, select_stmt, name="", cte=False, joins=None, with_clause=None):
        self.name = name
        self.select_stmt = select_stmt
        self.from_clause = None
        self.target = None
        self.where_clause = None
        self.with_clause = with_clause
        self.sort_clause = None
        self.limit = None
        self.rarg = None
        self.larg = None
        self.cte = cte
        self.recursive_part = None
        self.joins = joins

        if "larg" in self.select_stmt.keys() or "rarg" in self.select_stmt.keys():
            self.larg = SelectStmt(
                self.select_stmt["larg"]["SelectStmt"], self.name, self.cte)
            self.rarg = SelectStmt(
                self.select_stmt["rarg"]["SelectStmt"], self.name, self.cte)
            self.recursive_part = Recursive(self.larg, self.rarg, self.cte, self.name)
        else:

            for clause in self.select_stmt:
                if clause == "fromClause":
                    self.from_clause = FromClause(self.select_stmt[clause], self.name)
                elif clause == "targetList":
                    self.target = Target(
                        self.select_stmt[clause], self.from_clause, self.cte, self.name)
                elif clause == "whereClause":
                    self.where_clause = WhereUpper(
                        self.select_stmt[clause], self.from_clause, self.cte, self.name)
                elif clause == "sortClause":
                    self.sort_clause = Sort(self.select_stmt[clause], self.cte, self.from_clause, self.name)
                elif clause == "limitCount":
                    self.limit = Limit(self.select_stmt[clause], self.cte)

    def get_from_clause(self):
        return self.from_clause

    def get_where_clause(self):
        return self.where_clause

    def get_target_list(self):
        return self.target

    def transform_into_cypher(self):
        res = ""

        if self.recursive_part:

            res += self.recursive_part.transform_into_cypher()

        else:

            res += self.from_clause.transform_into_cypher()

            if self.where_clause:
                res += self.where_clause.transform_into_cypher()

            if self.sort_clause:
                res += self.sort_clause.transform_into_cypher()

            res += self.target.transform_into_cypher()

            if self.limit:
                res += self.limit.transform_into_cypher()

            if self.cte:
                res += " AS " + self.name + "\n"

        return res
