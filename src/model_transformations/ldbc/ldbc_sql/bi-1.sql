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
