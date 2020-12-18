-- Not correct query because time interval filtering is not included yet

MATCH (mt : message_tag)-[mt_messageid_m_messageid]->(m : message)
MATCH (mt : message_tag)-[mt_tagid_t_tagid]->(t : tag)

-- because group by t: this is, in fact, difficult query to transform into cypher
-- because it relies on GROUP BY based on tag names

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