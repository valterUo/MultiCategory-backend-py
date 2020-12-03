
from model_transformations.query_transformations.parse_tree_trasformations.sql_to_cypher import SqlToCypher
from model_transformations.query_transformations.pgSQL.pgSQL import pgSQL


parse_tree = pgSQL("""select p_firstname, p_lastname, p_birthday, p_locationip, p_browserused, p_placeid, p_gender,  p_creationdate
from person p
where p_personid = 42374893274938;""").get_parse_tree()

# MATCH (n : person)
# WHERE n.p_personid = 42374893274938
# RETURN n.p_firstname, n.p_lastname, n.p_birthday, n.p_locationip, n.p_browserused, n.p_placeid, n.p_gender, n.p_creationdate

"""
fromClause relname aliasname -> (aliasname : relname)
if no aliasname then alias_mapping(relname) = aliasname

ColumnRef -> RETURN aliasname.ColumnRef
where aliasname = SelectStmt..aliasname or alias_mapping(SelectStmt..relname)

whereClause A_Expr lexpr .. rexpr -> WHERE laliasname.lexpr = raliasname.rexpr or constants with suitble type changes
if lexp or rexp have ColumnRef, then aliasname = SelectStmt..aliasname or alias_mapping(SelectStmt..relname)
"""
res = SqlToCypher(parse_tree).transform_into_cypher()
print(res)
