from model_transformations.query_transformations.parse_tree_trasformations.column import Column
#from model_transformations.query_transformations.parse_tree_trasformations.join import Join


class Where:

    def __init__(self, where_clause, from_clause, cte = False):
        self.where_clause = where_clause
        self.left = None
        self.operator = None
        self.right = None
        self.join = None
        self.from_clause = from_clause
        self.cte = cte

        left_side = self.where_clause["A_Expr"]["lexpr"]
        right_side = self.where_clause["A_Expr"]["rexpr"]
        self.operator = self.where_clause["A_Expr"]["name"][0]["String"]["str"]

        if "ColumnRef" in left_side.keys() and "ColumnRef" in right_side.keys() and not self.cte:

            self.join = None #Join(self.where_clause)

        else:

            if "ColumnRef" in left_side.keys():

                self.left = Column(left_side["ColumnRef"], self.from_clause)

            elif "A_Const" in left_side.keys():

                if "Float" in left_side["A_Const"]["val"].keys():
                    self.left = left_side["A_Const"]["val"]["Float"]["str"]
                elif "String" in left_side["A_Const"]["val"].keys():
                    self.left = left_side["A_Const"]["val"]["String"]["str"]
                elif "Integer" in left_side["A_Const"]["val"].keys():
                    self.left = left_side["A_Const"]["val"]["String"]["str"]

            if "ColumnRef" in right_side.keys():

                self.right = Column(right_side["ColumnRef"], self.from_clause)

            elif "A_Const" in right_side.keys():

                if "Float" in right_side["A_Const"]["val"].keys():
                    self.right = right_side["A_Const"]["val"]["Float"]["str"]
                elif "String" in right_side["A_Const"]["val"].keys():
                    self.right = right_side["A_Const"]["val"]["String"]["str"]
                elif "Integer" in right_side["A_Const"]["val"].keys():
                    self.right = right_side["A_Const"]["val"]["String"]["str"]

    def transform_into_cypher(self):
        res = ""
        return res
