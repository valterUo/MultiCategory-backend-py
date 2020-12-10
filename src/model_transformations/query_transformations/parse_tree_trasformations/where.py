from model_transformations.query_transformations.parse_tree_trasformations.alias_mapping import get_name_for_alias
from model_transformations.query_transformations.parse_tree_trasformations.column import Column
from external_database_connections.postgresql.postgres import Postgres
rel_db = Postgres("ldbcsf1")


class Where:

    """
    This class implements only filtering conditional where clauses. Where clauses that create joins between tables are handled in Join class.

    In practice this means that this class handles all other cases expect those where parse tree has ColumnRef on both left and right side and these ColumnRefs induce a valid
    edge in the graph schema.
    """

    def __init__(self, where_clause, from_clause, cte=False, cte_name=""):
        self.where_clause = where_clause
        self.left = None
        self.operator = None
        self.right = None
        self.joins = []
        self.from_clause = from_clause
        self.cte = cte
        self.cte_name = cte_name

        if "A_Expr" in self.where_clause.keys():

            left_side = self.where_clause["A_Expr"]["lexpr"]
            right_side = self.where_clause["A_Expr"]["rexpr"]
            self.operator = self.where_clause["A_Expr"]["name"][0]["String"]["str"]

            if "ColumnRef" in left_side.keys() and "ColumnRef" in right_side.keys():
                self.left = Column(
                    left_side["ColumnRef"], self.from_clause, self.cte, self.cte_name)
                self.right = Column(
                    right_side["ColumnRef"], self.from_clause, self.cte, self.cte_name)
                left_table = get_name_for_alias(
                    self.left.get_collection_alias())
                right_table = get_name_for_alias(
                    self.right.get_collection_alias())
                if left_table and right_table:
                    if left_table != right_table:
                        self.joins.append(self.where_clause["A_Expr"])
            else:
                if "ColumnRef" in left_side.keys():

                    self.left = Column(
                        left_side["ColumnRef"], self.from_clause, self.cte, self.cte_name)

                elif "A_Const" in left_side.keys():

                    if "Float" in left_side["A_Const"]["val"].keys():
                        self.left = left_side["A_Const"]["val"]["Float"]["str"]
                    elif "String" in left_side["A_Const"]["val"].keys():
                        self.left = left_side["A_Const"]["val"]["String"]["str"]
                    elif "Integer" in left_side["A_Const"]["val"].keys():
                        self.left = left_side["A_Const"]["val"]["String"]["str"]

                if "ColumnRef" in right_side.keys():

                    self.right = Column(
                        right_side["ColumnRef"], self.from_clause, self.cte, self.cte_name)

                elif "A_Const" in right_side.keys():

                    if "Float" in right_side["A_Const"]["val"].keys():
                        self.right = right_side["A_Const"]["val"]["Float"]["str"]
                    elif "String" in right_side["A_Const"]["val"].keys():
                        self.right = right_side["A_Const"]["val"]["String"]["str"]
                    elif "Integer" in right_side["A_Const"]["val"].keys():
                        self.right = right_side["A_Const"]["val"]["String"]["str"]

        elif "NullTest" in self.where_clause.keys():
            self.left = Column(
                self.where_clause["NullTest"]["arg"]["ColumnRef"], self.from_clause, self.cte, self.cte_name)
            self.operator = "IS"
            self.right = "NULL"

    def transform_into_cypher(self, add_where=True):
        res = ""
        if add_where:
            res = "WHERE "
        if type(self.left) == str:
            res += self.left
        else:
            res += self.left.transform_into_cypher() + " "
        res += self.operator + " "
        if type(self.right) == str:
            res += self.right
        else:
            res += self.right.transform_into_cypher()
        return res + "\n"

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right
