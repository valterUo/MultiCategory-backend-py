from external_database_connections.neo4j.neo4j import Neo4j
from external_database_connections.postgresql.postgres import Postgres
from model_transformations.query_language_transformations.SQL.components.recursive_cte import RECURSIVE_CTE
from model_transformations.query_language_transformations.SQL.components.sql_with_subquery import SQL_with_subquery
from model_transformations.query_language_transformations.SQL.sql import SQL

query1 = """
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
       AND t.t_name = :tag
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
       AND m.m_creationdate > :date
       AND t.t_name = :tag
     GROUP BY p.p_personid
)
   , person_score AS (
    SELECT coalesce(pti.personid, pms.personid) AS personid
         , CASE WHEN pti.personid IS NULL then 0 ELSE 100 END -- scored from interest in the given tag
         + coalesce(pms.message_score, 0) AS score
      FROM person_tag_interest pti
           FULL JOIN person_message_score pms ON (pti.personid = pms.personid)
)
SELECT p.personid AS "person.id"
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

query2 = """
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

query3 = """
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

query4 = """
/* Q11. Unrelated replies
\set country  '\'Germany\''
\set blacklist '\'{"also","Pope","that","James","Henry","one","Green"}\''::text[]
 */
WITH replies_w_tags AS (
    SELECT p.p_personid AS creatorid
         , r.m_messageid AS replyid
         , r.m_c_replyof AS replyof
         , r.m_content AS content
         , CASE
             WHEN count(pt.mt_tagid)=0 THEN ARRAY[]::bigint[] -- no tags for the message, so we return an empty array
             ELSE array_agg(pt.mt_tagid)
           END AS replyTags
      FROM place co -- country
         , place ci -- city
         , person p
         , message r -- reply
           LEFT JOIN message_tag pt ON (r.m_messageid = pt.mt_messageid)
     WHERE 1=1
        -- join
       AND co.pl_placeid = ci.pl_containerplaceid
       AND ci.pl_placeid = p.p_placeid
       AND p.p_personid = r.m_creatorid
        -- filter
       AND co.pl_name = :country
       AND r.m_c_replyof IS NOT NULL
       -- exclude messages by the blacklist.
       -- Note: we use string_to_array(trim(regexp_replace(...))) instead regexp_split_to_array to avoid translating "Foo." into {Foo,""},
       -- i.e. remove possible empty firts/last elements
       --AND NOT string_to_array(trim(regexp_replace(r.m_content, E'[[:space:],.?!()\r\n]+', ' ', 'g')), ' ') && :blacklist
     GROUP BY p.p_personid, r.m_messageid, r.m_c_replyof, r.m_content
)
-- blacklisting is done after the joins and country filter above as it tured out to be an expensive operation (in 1st option)
 -- first blacklisting option is to tokenize message as words and use word-based search
   , replies_blacklist_excluded_1 AS (
    SELECT *
      FROM replies_w_tags
     WHERE 1=1
        -- filter
       -- exclude messages by the blacklist.
       -- Note: we use string_to_array(trim(regexp_replace(...))) instead regexp_split_to_array to avoid translating "Foo." into {Foo,""},
       -- i.e. remove possible empty firts/last elements
       AND NOT string_to_array(trim(regexp_replace(content, E'[[:space:],.?!()rn]+', ' ', 'g')), ' ') && :blacklist
)
 -- second blacklisting option is done using pure string contains
   , replies_blacklist_excluded_2 AS (
    SELECT *
      FROM replies_w_tags r
           LEFT JOIN unnest(:blacklist) AS bl(word) ON (r.content like '%'||bl.word||'%')
     WHERE 1=1
       -- exclude messages by the blacklist.
       AND bl.word IS NULL
)
   , replies_not_sharing_tags_w_base_message AS (
    SELECT r.replyid
         , r.creatorid
      FROM replies_blacklist_excluded_2 r
         , message b -- base message of the reply
           LEFT JOIN message_tag pt ON (b.m_messageid = pt.mt_messageid)
     WHERE 1=1
        -- join
       AND r.replyof = b.m_messageid
        -- filter
     GROUP BY r.replyid, r.creatorid, r.replyTags
    HAVING NOT r.replyTags &&
           CASE
             WHEN count(pt.mt_tagid)=0 THEN ARRAY[]::bigint[] -- no tags for the message, so we return an empty array
             ELSE array_agg(pt.mt_tagid)
           END
)
SELECT r.creatorid AS "person.id"
     , t.t_name AS "tag.name"
     , count(l.l_messageid) as likeCount
     , count(DISTINCT r.replyid) as replyCount
     --, array_agg(DISTINCT r.replyid ORDER BY r.replyid) AS affectedReplyIds -- for debugging purposes
  FROM replies_not_sharing_tags_w_base_message r
       LEFT JOIN likes l ON (r.replyid = l.l_messageid)
     , message_tag pt
     , tag t
 WHERE 1=1
    -- join
   AND r.replyid = pt.mt_messageid
   AND pt.mt_tagid = t.t_tagid
 GROUP BY r.creatorid, t.t_name
 ORDER BY likeCount DESC, r.creatorid, t.t_name
 LIMIT 100
;
"""

recursive = """
with recursive cposts(m_messageid, m_content, m_ps_imagefile, m_creationdate, m_c_replyof, m_creatorid) AS (
	  select m_messageid, m_content, m_ps_imagefile, m_creationdate, m_c_replyof, m_creatorid
	  from message
	  where m_creatorid = :personId
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
     ) p2  
     on p2.orig_postid = p1.m_messageid
      order by m_creationdate desc, p2.m_messageid desc;
"""

short = """
select m_messageid, m_c_replyof, orig_postid, m_creatorid
       from message, parent
       where m_messageid=replyof
"""

testt = """
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

small = """select orig_postid, postid as m_messageid, p_personid, p_firstname, p_lastname
      from parent, person
      where replyof is null and creator = p_personid"""

main_subquery = """
select p1.m_messageid, COALESCE(m_ps_imagefile,'')||COALESCE(m_content,''), p1.m_creationdate,
        p2.m_messageid, p2.p_personid, p2.p_firstname, p2.p_lastname
 from 
      p1 
      left join p2
      on p1.m_messageid = p2.orig_postid
       order by m_creationdate desc, p2.m_messageid desc;"""


query = """
/* Q1. Posting summary
\set date '\'2011-07-21T22:00:00.000+00:00\''::timestamp
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

db = Postgres("ldbcsf1")

elem = SQL("test", main_subquery, db)
print(elem.get_cypher())

# elem = RECURSIVE_CTE("test", recursive, db)
# print(elem.get_cypher())

# elem = SQL_with_subquery("test", main_subquery, db)
# print(elem.get_cypher())

# graph_db = Neo4j("ldbcsf1")
# graph_db.transform_tables_into_graph_db(db)
# graph_db.create_edges(db)
