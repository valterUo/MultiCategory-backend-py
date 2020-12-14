
from model_transformations.query_transformations.parse_tree_trasformations.sql_to_cypher import SqlToCypher
from model_transformations.query_transformations.pgSQL.pgSQL import pgSQL
import json
import os
import glob

simple1 = """
select p_firstname, p_lastname, p_birthday, p_locationip, p_browserused, p_placeid, p_gender,  p_creationdate
from person p
where (p_personid = 42374893274938 or p_locationip = '0.0.0.0') and p_lastname = 'Anna';
"""

simple2 = """
with recursive cposts(m_messageid, m_content, m_ps_imagefile, m_creationdate, m_c_replyof, m_creatorid) AS (
	  select m_messageid, m_content, m_ps_imagefile, m_creationdate, m_c_replyof, m_creatorid
	  from message
	  where m_creatorid = 42374893274938
	  order by m_creationdate desc
	  limit 10
), parent(postid, replyof, orig_postid, creator) AS (
	  select m_messageid, m_c_replyof, m_messageid, m_creatorid from cposts
	UNION ALL
	  select m_messageid, m_c_replyof, orig_postid, m_creatorid
      from message, parent
      where m_messageid = replyof
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
     ) p2  
     on p2.orig_postid = p1.m_messageid
      order by m_creationdate desc, p2.m_messageid desc;
"""

#parse_tree = pgSQL(simple2).get_parse_tree()

# with open("C://Users//Valter Uotila//Desktop//NLP//test4.json", "w+") as json_file:
#     json.dump(parse_tree, json_file)

dirname = os.path.dirname(__file__)
example_files_path = os.path.join(dirname, "..//..//..//model_transformations//ldbc//ldbc_sql//*.sql")
example_filenames = glob.glob(example_files_path)
for file_name in example_filenames:
      with open(file_name, 'r') as reader:
            lines = reader.read()
            parse_tree = pgSQL(lines).get_parse_tree()
            with open("C://Users//Valter Uotila//Desktop//parsed_ldbc_queries//" + os.path.basename(file_name) + ".json", "w+") as json_file:
                  json.dump(parse_tree, json_file)
                  
#res = SqlToCypher(parse_tree).transform_into_cypher()
#print(res)
