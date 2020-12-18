MATCH (co : place)
MATCH (t : tag)-[t_tagclassid_tc_tagclassid]->(tc : tagclass)
MATCH (pt : message_tag)-[mt_tagid_t_tagid]->(t : tag)
MATCH (pt : message_tag)-[mt_messageid_m_messageid]->(p : message)
MATCH (f : forum)-[f_moderatorid_p_personid]->(m : person)
MATCH (m : person)-[p_placeid_pl_placeid]->(ci : place)
WHERE 1= 1
AND p.m_ps_forumid = f.f_forumid
AND ci.pl_containerplaceid = co.pl_placeid
AND tc.tc_name = "MusicalArtist"
AND co.pl_name = "Burma"
WITH f, count(distinct p.m_messageid) AS c4
RETURN f.f_forumid AS forum_id, f.f_title AS forum_title, f.f_creationdate AS forum_creationDate, f.f_moderatorid AS person_id, c4 AS postcount
ORDER BY postcount DESC, f.f_forumid ASC

LIMIT 20