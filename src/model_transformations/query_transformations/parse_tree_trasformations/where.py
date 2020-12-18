from model_transformations.query_transformations.parse_tree_trasformations.column import Column
from model_transformations.query_transformations.parse_tree_trasformations.typecast import pg_types_to_neo4j_types


class Where:

    """
    This class implements only filtering conditional where clauses. Where clauses that create joins between tables are handled in Join class.

    In practice this means that this class handles all other cases expect those where parse tree has ColumnRef on both left and right side and these ColumnRefs induce a valid
    edge in the graph schema.

    /*
        * A_Expr - infix, prefix, and postfix expressions
    */
        typedef enum A_Expr_Kind
        {
            AEXPR_OP,                   /* 0 normal operator */
            AEXPR_OP_ANY,               /* 1 scalar op ANY (array) */
            AEXPR_OP_ALL,               /* 2 scalar op ALL (array) */
            AEXPR_DISTINCT,             /* 3 IS DISTINCT FROM - name must be "=" */
            AEXPR_NOT_DISTINCT,         /* 4 IS NOT DISTINCT FROM - name must be "=" */
            AEXPR_NULLIF,               /* 5 NULLIF - name must be "=" */
            AEXPR_IN,                   /* 6 [NOT] IN - name must be "=" or "<>" */
            AEXPR_LIKE,                 /* 7 [NOT] LIKE - name must be "~~" or "!~~" */
            AEXPR_ILIKE,                /* 8 [NOT] ILIKE - name must be "~~*" or "!~~*" */
            AEXPR_SIMILAR,              /* 9 [NOT] SIMILAR - name must be "~" or "!~" */
            AEXPR_BETWEEN,              /* 10 name must be "BETWEEN" */
            AEXPR_NOT_BETWEEN,          /* 11 name must be "NOT BETWEEN" */
            AEXPR_BETWEEN_SYM,          /* 12 name must be "BETWEEN SYMMETRIC" */
            AEXPR_NOT_BETWEEN_SYM       /* 13 name must be "NOT BETWEEN SYMMETRIC" */
        } A_Expr_Kind;

    """

    def __init__(self, where_clause, from_clause, cte=False, cte_name=""):
        #print(json.dumps(where_clause, indent = 2))
        self.where_clause = where_clause
        self.left = None
        self.operator = None
        self.right = None
        self.joins = []
        self.from_clause = from_clause
        self.cte = cte
        self.cte_name = cte_name
        self.type = None
        self.left_side_typecasted = False
        self.right_side_typecasted = False
        self.kind = None

        if "A_Expr" in self.where_clause.keys():

            self.left_side = self.where_clause["A_Expr"]["lexpr"]
            self.right_side = self.where_clause["A_Expr"]["rexpr"]
            self.operator = self.where_clause["A_Expr"]["name"][0]["String"]["str"]
            self.kind = self.where_clause["A_Expr"]["kind"]

            if self.kind == 0:

                if type(self.left_side) == dict and type(self.right_side) == dict:

                    if "ColumnRef" in self.left_side.keys() and "ColumnRef" in self.right_side.keys():

                        self.left = Column(
                            self.left_side["ColumnRef"], self.from_clause, self.cte, self.cte_name)

                        self.right = Column(
                            self.right_side["ColumnRef"], self.from_clause, self.cte, self.cte_name)

                    else:
                        if "ColumnRef" in self.left_side.keys():

                            self.left = Column(
                                self.left_side["ColumnRef"], self.from_clause, self.cte, self.cte_name)

                        elif "A_Const" in self.left_side.keys():

                            self.left = self.handle_a_const(self.left_side)

                        elif "TypeCast" in self.left_side.keys():
                            self.left, self.type = self.handle_typecast(
                                self.left_side)
                            self.left_side_typecasted = True

                        if "ColumnRef" in self.right_side.keys():

                            self.right = Column(
                                self.right_side["ColumnRef"], self.from_clause, self.cte, self.cte_name)

                        elif "A_Const" in self.right_side.keys():
                            self.right = self.handle_a_const(self.right_side)

                        elif "TypeCast" in self.right_side.keys():
                            self.right, self.type = self.handle_typecast(
                                self.right_side)
                            self.right_side_typecasted = True

            elif self.kind == 7:

                if type(self.left_side) == dict and type(self.right_side) == list:

                    if "ColumnRef" in self.left_side.keys():
                        self.left = Column(
                            self.left_side["ColumnRef"], self.from_clause, self.cte, self.cte_name)

                    self.right = []
                    for elem in self.right_side:
                        if "A_Const" in elem.keys():
                            self.right.append(self.handle_a_const(elem))
                        elif "TypeCast" in elem.keys():
                            res, self.type = self.handle_typecast(
                                self.right_side)
                            self.right.append(res)
                            self.right_side_typecasted = True

            elif self.kind == 11:

                if type(self.left_side) == dict and type(self.right_side) == list:
                    if "ColumnRef" in self.left_side.keys():
                        self.left = Column(
                            self.left_side["ColumnRef"], self.from_clause, self.cte, self.cte_name)

                    self.right = []
                    for elem in self.right_side:
                        if "A_Const" in elem.keys():
                            self.right.append(self.handle_a_const(elem))
                        elif "TypeCast" in elem.keys():
                            res, self.type = self.handle_typecast(elem)
                            self.right.append(res)
                            self.right_side_typecasted = True

        elif "NullTest" in self.where_clause.keys():
            self.kind = "nulltest"
            self.left = Column(
                self.where_clause["NullTest"]["arg"]["ColumnRef"], self.from_clause, self.cte, self.cte_name)
            self.operator = "IS"
            self.right = "NULL"

    def transform_into_cypher(self, add_where=True):
        res = ""
        if self.left and self.right:
            if add_where:
                res = "WHERE "

            """
            Left side of the single where clause
            """

            if self.kind == 11:
                if self.operator == "BETWEEN":
                    if self.type == "timestamp":
                        if len(self.right) == 2:

                            """
                            Strange but Neo4j lacks datetime comparisions. Transforming datetimes into integers and comparing them is the workaround here.
                            """

                            res += self.right[0] + ".epochMillis " + " <= " + pg_types_to_neo4j_types(self.type,
                                                    self.left.transform_into_cypher(), "column") + ".epochMillis <= " + self.right[1] +".epochMillis" + "\n"
            else:

                if type(self.left) == str:
                    res += '"' + str(self.left) + '"'
                elif type(self.left) == int:
                    res += str(self.left)
                else:
                    if self.right_side_typecasted:
                        res += pg_types_to_neo4j_types(self.type,
                                                    self.left.transform_into_cypher(), "column") + " "
                    else:
                        res += self.left.transform_into_cypher() + " "

                """
                Operator i.e. equality, inequality or other comparision, inclusion etc.
                Most of the time Postgres and Neo4j have same naming here.
                """

                if self.kind == 7:
                    res += "IN "
                else:
                    res += self.operator + " "

                """
                Right side of the single where clause
                """

                if type(self.right) == str:
                    res += '"' + str(self.right) + '"'
                elif type(self.right) == int:
                    res += str(self.right)
                elif type(self.right) == list:
                    if self.kind == 7:
                        res += "["
                        for elem in self.right:
                            res += "'" + elem + "'" + ", "
                        res = res[0:-2] + "]"
                else:
                    if self.left_side_typecasted:
                        res += pg_types_to_neo4j_types(self.type,
                                                    self.right.transform_into_cypher(), "column") + " "
                    else:
                        res += self.right.transform_into_cypher()
                return res + "\n"

        return res + "\n"

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def handle_a_const(self, elem):
        temp = elem["A_Const"]["val"]
        if "Float" in temp.keys():
            return temp["Float"]["str"]
        elif "String" in temp.keys():
            return temp["String"]["str"]
        elif "Integer" in temp.keys():
            return temp["Integer"]["ival"]

    def handle_typecast(self, elem):
        value = elem["TypeCast"]["arg"]["A_Const"]["val"]["String"]["str"]
        type = elem["TypeCast"]["typeName"]["TypeName"]["names"][-1]["String"]["str"]
        result = pg_types_to_neo4j_types(type, value)
        return result, type
