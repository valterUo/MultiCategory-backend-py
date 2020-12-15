from model_transformations.query_transformations.parse_tree_trasformations.column import Column
from model_transformations.query_transformations.parse_tree_trasformations.func_call import FuncCall


class AExpression:

    def __init__(self, left, operator, right, from_clause=None, cte=None, cte_name=None, rename=None):
        self.left_initial = left
        self.left = None
        self.operator = operator
        self.right_initial = right
        self.right = None
        self.col_refer = None
        self.expr = None

        self.from_clause = from_clause
        self.cte = cte
        self.cte_name = cte_name
        self.rename = rename

        if "A_Const" in self.left_initial.keys():
            temp_left = self.left_initial["A_Const"]["val"]
            if "String" in temp_left:
                self.left = temp_left["String"]["str"]
            elif "Integer" in temp_left:
                self.left = temp_left["Integer"]["ival"]
            elif "Float" in temp_left:
                self.left = temp_left["Float"]["str"]
        elif "FuncCall" in self.left_initial.keys():
            self.left = FuncCall(
                self.left_initial["FuncCall"], self.from_clause, self.cte, self.cte_name, self.rename)
            self.col_refer = self.left.get_col_refer()
        elif "ColumnRef" in self.left_initial.keys():
            self.left = Column(
                self.left_initial["ColumnRef"], self.from_clause, True, self.cte_name, self.rename)

        if "A_Const" in self.right_initial.keys():
            temp_right = self.right_initial["A_Const"]["val"]
            if "String" in temp_right:
                self.right = temp_right["String"]["str"]
            elif "Integer" in temp_right:
                self.right = temp_right["Integer"]["ival"]
            elif "Float" in temp_right:
                self.right = temp_right["Float"]["str"]
        elif "FuncCall" in self.right_initial.keys():
            self.right = FuncCall(
                self.right_initial["FuncCall"], self.from_clause, self.cte, self.cte_name, self.rename)
            self.col_refer = self.right.get_col_refer()
        elif "ColumnRef" in self.right_initial.keys():
            self.right = Column(
                self.right_initial["ColumnRef"], self.from_clause, True, self.cte_name, self.rename)

    def transform_into_cypher(self, with_with=True):
        res = ""
        if with_with:
            res += "WITH *, "
        if self.left and self.right:
            if type(self.left) == str or type(self.left) == int:
                res += str(self.left) + " "
            else:
                res += self.left.transform_into_cypher(with_with=False) + " "

            res += self.operator + " "

            if type(self.right) == str or type(self.right) == int:
                res += str(self.right)
            else:
                res += self.right.transform_into_cypher(with_with=False)
            if with_with:
                res += " AS " + self.col_refer.get_field()
        return res

    def get_col_refer(self):
        return self.col_refer
