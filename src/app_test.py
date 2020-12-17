
from model_transformations.query_transformations.parse_tree_trasformations.sql_to_cypher import SqlToCypher
from model_transformations.query_transformations.pgSQL.pgSQL import pgSQL

query = """
WITH detail AS (
   SELECT
      t.t_name,
      count(
         DISTINCT CASE
            WHEN extract(
               MONTH
               FROM
                  m.m_creationdate
            ) = 11 THEN m.m_messageid
            ELSE NULL
         END
      ) AS countMonth1,
      count(
         DISTINCT CASE
            WHEN extract(
               MONTH
               FROM
                  m.m_creationdate
            ) != 11 THEN m.m_messageid
            ELSE NULL
         END
      ) AS countMonth2
   FROM
      message m,
      message_tag mt,
      tag t
   WHERE
      1 = 1 -- join
      AND m.m_messageid = mt.mt_messageid
      AND mt.mt_tagid = t.t_tagid -- filter
      AND m.m_creationdate >= make_date(2010, 11, 1)
      AND m.m_creationdate < make_date(2010, 11, 1) + make_interval(months => 2)
   GROUP BY
      t.t_name
)
SELECT
   t_name AS "tag_name",
   countMonth1,
   countMonth2,
   abs(countMonth1 - countMonth2) AS diff
FROM
   detail d
ORDER BY
   diff DESC,
   t_name
LIMIT
   100;
"""

parse_tree = pgSQL(query).get_parse_tree()

res = SqlToCypher(parse_tree).transform_into_cypher()
print(res)

"""
MATCH (mt : message_tag)-[mt_messageid_m_messageid]->(m : message)
MATCH (mt : message_tag)-[mt_tagid_t_tagid]->(t : tag)
-- because group by t
WITH t, count(distinct CASE
WHEN datetime(m.m_creationdate).month = 11 THEN m.m_messageid
ELSE NULL
END) AS c1

MATCH (mt : message_tag)-[mt_messageid_m_messageid]->(m : message)
MATCH (mt : message_tag)-[mt_tagid_t_tagid]->(t : tag)

WITH c1, t, count(distinct CASE
WHEN datetime(m.m_creationdate).month <> 11 THEN m.m_messageid
ELSE NULL
END) AS c2

WITH collect({ t_name : t.t_name, countmonth1: c1, countmonth2 : c2 }) as detail

UNWIND detail as d
WITH *, abs(d.countmonth1 - d.countmonth2) AS func3
RETURN d.t_name AS tag_name, d.countmonth1, d.countmonth2, func3 AS diff
ORDER BY diff DESC, d.t_name ASC
LIMIT 100

"""
