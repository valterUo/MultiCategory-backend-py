from external_database_connections.neo4j.neo4j import Neo4j
from external_database_connections.postgresql.postgres import Postgres
from model_transformations.query_language_transformations.SQL.sql import SQL

query3 = """
/* Q10. Central Person for a Tag
\set tag '\'Che_Guevara\''
\set date '\'2011-07-22T00:00:00.000+00:00\''::timestamp
 */
WITH person_tag_interest AS (
    SELECT p.p_personid AS personid
      FROM person p
         , person_tag pt
         , tag t
     WHERE 1=1
        -- join
       AND p.p_personid = pt.pt_personid
       AND pt.pt_tagid = t.t_tagid
        -- filter
       AND t.t_name = 'Che_Guevara'
)
   , person_message_score AS (
    SELECT p.p_personid AS personid
         , count(*) AS message_score
      FROM message m
         , person p
         , message_tag pt
         , tag t
     WHERE 1=1
        -- join
       AND m.m_creatorid = p.p_personid
       AND m.m_messageid = pt.mt_messageid
       AND pt.mt_tagid = t.t_tagid
        -- filter
       AND m.m_creationdate > datetime('2011-07-22')
       AND t.t_name = 'Che_Guevara'
     GROUP BY p.p_personid
)
   , person_score AS (
    SELECT coalesce(pti.personid, pms.personid) AS personid
         , CASE WHEN pti.personid IS NULL then 0 ELSE 100 END -- scored from interest in the given tag
         + coalesce(pms.message_score, 0) AS score
      FROM person_tag_interest pti
           FULL JOIN person_message_score pms ON (pti.personid = pms.personid)
)
SELECT p.personid AS personid
     , p.score AS score
     , sum(f.score) AS friendsScore
  FROM person_score p
     , knows k
     , person_score f -- the friend
 WHERE 1=1
    -- join
   AND p.personid = k.k_person1id
   AND k.k_person2id = f.personid
 GROUP BY p.personid, p.score
 ORDER BY p.score + sum(f.score) DESC, p.personid
 LIMIT 100
;
"""

query1 = """
SELECT p.p_personid AS personid
      FROM person p
         , person_tag pt
         , tag t
     WHERE 1=1
        -- join
       AND p.p_personid = pt.pt_personid
       AND pt.pt_tagid = t.t_tagid
        -- filter
       AND t.t_name = 'Che_Guevara'
"""

query1 = """
/* Q12. Trending Posts
The query originally from: https://github.com/ldbc/ldbc_snb_implementations/blob/dev/postgres/queries/bi-12.sql
\set date '\'2011-07-22T00:00:00.000+00:00\''::timestamp
\set likeThreshold 400
 */
SELECT m.m_messageid AS "message.id"
     , m.m_creationdate AS "message.creationDate"
     , c.p_firstname AS "creator.firstName"
     , c.p_lastname AS "creator.lastName"
     , count(*) as likeCount
  FROM message m
     , person c -- creator
     , likes l
 WHERE 1=1
    -- join
   AND m.m_creatorid = c.p_personid
   AND m.m_messageid = l.l_messageid
    -- filter
   AND m.m_creationdate > :date
 GROUP BY m.m_messageid
        , m.m_creationdate
        , c.p_firstname
        , c.p_lastname
HAVING count(*) > :likeThreshold
 ORDER BY likeCount DESC, m.m_messageid
 LIMIT 100;
"""

query = """
/* Q1. Posting summary
\set date '2011-07-21T22:00:00.000+00:00::timestamp
 */
WITH 
  message_count AS (
    SELECT 0.0 + count(*) AS cnt
      FROM message
     WHERE 1=1
       AND m_creationdate < :date
)
, message_prep AS (
    SELECT extract(year from m_creationdate) AS messageYear
         , m_c_replyof IS NOT NULL AS isComment
         , CASE
             WHEN m_length <  40 THEN 0 -- short
             WHEN m_length <  80 THEN 1 -- one liner
             WHEN m_length < 160 THEN 2 -- tweet
             ELSE                     3 -- long
           END AS lengthCategory
         , m_length
      FROM message
     WHERE 1=1
       AND m_creationdate < :date
       --AND m_content IS NOT NULL
       AND m_ps_imagefile IS NULL -- FIXME CHECKME: posts w/ m_ps_imagefile IS NOT NULL should have m_content IS NULL
)
SELECT messageYear, isComment, lengthCategory
     , count(*) AS messageCount
     , avg(m_length) AS averageMessageLength
     , sum(m_length) AS sumMessageLength
     , count(*) / mc.cnt AS percentageOfMessages
  FROM message_prep
     , message_count mc
 GROUP BY messageYear, isComment, lengthCategory, mc.cnt
 ORDER BY messageYear DESC, isComment ASC, lengthCategory ASC
;

"""

difficult = """
SELECT extract(year from m_creationdate) AS messageYear
         , m_c_replyof IS NOT NULL AS isComment
         , CASE
             WHEN m_length <  40 THEN 0
             WHEN m_length <  80 THEN 1
             WHEN m_length < 160 THEN 2
             ELSE                     3
           END AS lengthCategory
         , m_length
      FROM message
     WHERE 1=1
       AND m_creationdate < :date
       AND m_ps_imagefile IS NULL
"""

simple = """
select p_firstname, p_lastname, p_birthday, p_locationip, p_browserused, p_placeid, p_gender,  p_creationdate
from person
where p_personid = :personId;
"""

simple2 = """
select p_personid, p_firstname, p_lastname, k_creationdate
from knows, person
where k_person1id = :personId 
and k_person2id = p_personid
order by k_creationdate desc, p_personid asc;
"""

subquery = """
select p2.m_messageid, p2.m_content, p2.m_creationdate, p_personid, p_firstname, p_lastname,
    (case when exists (
     	   	       select 1 from knows
		       where p1.m_creatorid = k_person1id and p2.m_creatorid = k_person2id)
      then TRUE
      else FALSE
      end)
from message p1, message p2, person
where
  p1.m_messageid = :messageId and p2.m_c_replyof = p1.m_messageid and p2.m_creatorid = p_personid
order by p2.m_creationdate desc, p2.m_creatorid asc;"""

query = """
select p_personid, p_firstname, p_lastname, m_messageid, COALESCE(m_ps_imagefile, m_content, ''), m_creationdate
from person, message, knows
where
    p_personid = m_creatorid and
    m_creationdate < :maxDate and
    k_person1id = :personId and
    k_person2id = p_personid
order by m_creationdate desc, m_messageid asc
limit 20
"""

print()

db = Postgres("ldbcsf1")

elem = SQL("test", query, db)
print(elem.get_cypher(elem))


# graph_db = Neo4j("ldbcsf1")
# graph_db.transform_tables_into_graph_db(db)
# graph_db.create_edges(db)