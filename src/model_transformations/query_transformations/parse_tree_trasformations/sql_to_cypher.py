from model_transformations.query_transformations.parse_tree_trasformations.select_stmt import SelectStmt


class SqlToCypher:

    """
    fromClause relname aliasname -> (aliasname : relname)
    if no aliasname then alias_mapping(relname) = aliasname

    ColumnRef -> RETURN aliasname.ColumnRef
    where aliasname = SelectStmt..aliasname or alias_mapping(SelectStmt..relname)

    whereClause A_Expr lexpr .. rexpr -> WHERE laliasname.lexpr = raliasname.rexpr or constants with suitble type changes
    if lexp or rexp have ColumnRef, then aliasname = SelectStmt..aliasname or alias_mapping(SelectStmt..relname)
    """

    def __init__(self, sql_parse_tree):
        self.sql_parse_tree = sql_parse_tree
        self.transformed_stmt = []
        for elem in sql_parse_tree:
            if "RawStmt" in elem:
                if "stmt" in elem["RawStmt"]:
                    for substmt in elem["RawStmt"]["stmt"]:
                        if substmt == "SelectStmt":
                            self.transformed_stmt.append(SelectStmt(elem["RawStmt"]["stmt"]["SelectStmt"]))

    def transform_into_cypher(self):
        res = ""
        for elem in self.transformed_stmt:
            res += elem.transform_into_cypher()
        return res
