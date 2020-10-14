MATCH (pt : person_tag) -[pt_personid_p_personid]-> (p : person) 
MATCH (pt : person_tag) -[pt_tagid_t_tagid]-> (t : tag)
WHERE 1=1 AND
t.t_name = 'Che_Guevara'
WITH collect({ personid : p.p_personid }) AS person_tag_interest

MATCH (m : message) -[m_creatorid_p_personid]-> (p : person)
MATCH  (pt : message_tag) -[mt_messageid_m_messageid]-> (m : message)
MATCH (pt : message_tag) -[mt_tagid_t_tagid]-> (t : tag)
WHERE 1=1 AND
datetime(m.m_creationdate) > datetime('2011-07-22') AND
t.t_name =  'Che_Guevara'
WITH count(*) AS count_var, p, person_tag_interest
WITH collect({ personid : p.p_personid, message_score: count_var }) AS person_message_score, person_tag_interest AS person_tag_interest

UNWIND person_tag_interest AS pti
UNWIND person_message_score AS pms
WITH pms, pti, person_tag_interest, person_message_score
WHERE pti.personid = pms.personid
WITH collect({ personid : coalesce(pti.personid, pms.personid), score : case when pti.personid is null then 0 else 100 end + coalesce(pms.message_score, 0) }) AS person_score

UNWIND person_score AS p
//WITH DISTINCT p
MATCH (k : knows)
UNWIND person_score AS f
WITH f, p
WHERE p.personid = k.k_person1id AND
k.k_person2id = f.personid AND
1=1
RETURN p.personid AS personid, p.score AS score, sum(f.score) AS friendsscore
ORDER BY  p.score + sum(f.score) desc, p.personid