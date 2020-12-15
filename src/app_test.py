
from model_transformations.query_transformations.parse_tree_trasformations.sql_to_cypher import SqlToCypher
from model_transformations.query_transformations.pgSQL.pgSQL import pgSQL
import json
import os
import glob

query = """
SELECT
   co.pl_name AS "country_name",
   extract(
      MONTH
      FROM
         p.m_creationdate
   ) AS messageMonth,
   cr.p_gender AS "person_gender",
--   floor(
--      extract(
--         YEARS
--         FROM
--            age('2013-01-01' :: date, cr.p_birthday)
--      ) / 5
--   ) AS ageGroup,
   t.t_name AS "tag_name",
   count(*) AS messageCount
FROM
   message p,
   message_tag pt,
   tag t,
   person cr, -- creator
   place ci, -- city
   place co -- country
WHERE
   1 = 1 -- join
   AND p.m_messageid = pt.mt_messageid
   AND pt.mt_tagid = t.t_tagid
   AND p.m_creatorid = cr.p_personid
   AND cr.p_placeid = ci.pl_placeid
   AND ci.pl_containerplaceid = co.pl_placeid -- filter
   AND co.pl_name IN ('Ethiopia', 'Belarus')
   AND p.m_creationdate BETWEEN '2010-01-01T00:00:00.000+00:00' :: timestamp
   AND '2010-11-08T00:00:00.000+00:00' :: timestamp
GROUP BY
   co.pl_name,
   messageMonth,
   cr.p_gender,
   t.t_name,
   ageGroup
HAVING
   count(*) > 100
LIMIT
   100;
"""

parse_tree = pgSQL(query).get_parse_tree()

res = SqlToCypher(parse_tree).transform_into_cypher()
print(res)

# with open("C://Users//Valter Uotila//Desktop//NLP//test4.json", "w+") as json_file:
#     json.dump(parse_tree, json_file)

# dirname = os.path.dirname(__file__)
# example_files_path = os.path.join(dirname, "model_transformations//ldbc//ldbc_sql//*.sql")
# example_filenames = glob.glob(example_files_path)
# for file_name in example_filenames:
#       print(file_name)
#       with open(file_name, 'r') as reader:
#             lines = reader.read()
#             parse_tree = pgSQL(lines).get_parse_tree()
#             print(len(parse_tree))
#             with open("C://Users//Valter Uotila//Desktop//parsed_ldbc_queries//" + os.path.basename(file_name) + ".json", "w+") as json_file:
#                   json.dump(parse_tree, json_file)
