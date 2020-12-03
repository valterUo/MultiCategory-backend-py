from model_transformations.query_transformations.parse_tree_trasformations.select_stmt_transformation import SelectStmt


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
        self.cypher_parse_tree = None
        self.transformed_stmt = []
        for elem in sql_parse_tree:
            if "RawStmt" in elem:
                self.transformed_stmt += self.transform_rawstmt(elem["RawStmt"])

    def transform_rawstmt(self, rawstmt):
        if "stmt" in rawstmt:
            return self.transform_stmt(rawstmt["stmt"])
    
    def transform_stmt(self, stmt):
        res = []
        for substmt in stmt:
            if substmt == "SelectStmt":
                res.append(SelectStmt(stmt["SelectStmt"]))
        return res
    
    def transform_into_cypher(self):
        res = ""
        for elem in self.transformed_stmt:
            res += elem.transform_into_cypher()
        return res
