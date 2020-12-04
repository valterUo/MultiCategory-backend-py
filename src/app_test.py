
from model_transformations.query_transformations.parse_tree_trasformations.sql_to_cypher import SqlToCypher
from model_transformations.query_transformations.pgSQL.pgSQL import pgSQL
import json

simple1 = """
select p_firstname, p_lastname, p_birthday, p_locationip, p_browserused, p_placeid, p_gender,  p_creationdate
from person p
where p_personid = 42374893274938;
"""

simple2 = """
with recursive cposts(m_messageid, m_content, m_ps_imagefile, m_creationdate, m_c_replyof, m_creatorid) AS (
	  select m_messageid, m_content, m_ps_imagefile, m_creationdate, m_c_replyof, m_creatorid
	  from message
	  where m_creatorid = 42374893274938
	  order by m_creationdate desc
	  limit 10
), parent(postid,replyof,orig_postid,creator) AS (
	  select m_messageid, m_c_replyof, m_messageid, m_creatorid from cposts
	UNION ALL
	  select m_messageid, m_c_replyof, orig_postid, m_creatorid
      from message,parent
      where m_messageid=replyof
)
select p1.m_messageid, COALESCE(m_ps_imagefile,'')||COALESCE(m_content,''), p1.m_creationdate,
       p2.m_messageid, p2.p_personid, p2.p_firstname, p2.p_lastname
from 
     (select m_messageid, m_content, m_ps_imagefile, m_creationdate, m_c_replyof from cposts
     ) p1
     left join
     (select orig_postid, postid as m_messageid, p_personid, p_firstname, p_lastname
      from parent, person
      where replyof is null and creator = p_personid
     )p2  
     on p2.orig_postid = p1.m_messageid
      order by m_creationdate desc, p2.m_messageid desc;
"""


parse_tree = pgSQL(simple2).get_parse_tree()

# with open("C:\\Users\\Valter Uotila\\Desktop\\NLP\\test2.json", "w+") as json_file:
#     json.dump(parse_tree, json_file)

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
