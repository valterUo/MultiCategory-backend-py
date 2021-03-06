MATCH (pt : person_tag) -[pt_personid_p_personid]-> (p : person)
MATCH (pt : person_tag) -[pt_tagid_t_tagid]-> (t : tag)
WHERE 1=1 AND 
t.t_name =:tag
WITH p
WITH collect({ personid : p.p_personid}) AS person_tag_interest

MATCH (m : message) -[m_creatorid_p_personid]-> (p : person)
MATCH (pt : message_tag) -[mt_messageid_m_messageid]-> (m : message)
MATCH (pt : message_tag) -[mt_tagid_t_tagid]-> (t : tag)
WHERE 1=1 AND 
datetime(m.m_creationdate)>:date AND 
t.t_name =:tag
WITH count(*) AS fvu, person_tag_interest, p
WITH person_tag_interest, collect({ personid : p.p_personid, message_score : fvu}) AS person_message_score

UNWIND person_tag_interest AS pti
UNWIND person_message_score AS pms
WITH person_tag_interest, person_message_score, pti, pms
WHERE pti.personid = pms.personid
WITH person_tag_interest, person_message_score, pti, pms
WITH person_tag_interest, person_message_score, collect({ personid : coalesce(pti.personid, pms.personid), score : case when pti.personid is null then 0 else 100 end + coalesce(pms.message_score, 0)}) AS person_score

UNWIND person_score AS p
MATCH (k : knows)
UNWIND person_score AS f
WITH p, f
WHERE p.personid = k.k_person1id
AND k.k_person2id = f.personid
AND 1=1
RETURN p.personid AS person_id, p.score AS score, sum(f.score) AS friendsscore
ORDER BY p.score + sum(f.score) desc, p.personid
LIMIT  100