MATCH (co : place)
MATCH (pt : message_tag)-[mt_messageid_m_messageid]->(p : message)
MATCH (pt : message_tag)-[mt_tagid_t_tagid]->(t : tag)
MATCH (p : message)-[m_creatorid_p_personid]->(cr : person)
MATCH (cr : person)-[p_placeid_pl_placeid]->(ci : place)
WHERE 1= 1
AND ci.pl_containerplaceid = co.pl_placeid
AND co.pl_name IN ['Ethiopia', 'Belarus']
AND datetime('2010-01-01T00:00:00.000+00:00').epochMillis  <= datetime(p.m_creationdate).epochMillis <= datetime('2010-11-08T00:00:00.000+00:00').epochMillis
WITH *, count(*) AS c4
RETURN co.pl_name AS country_name, datetime(p.m_creationdate).month AS messagemonth, cr.p_gender AS person_gender, t.t_name AS tag_name, c4 AS messagecount
LIMIT 100