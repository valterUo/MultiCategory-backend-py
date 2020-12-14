/* Q2. Top tags for country, age, gender, time
 \set startDate '\'2010-01-01T00:00:00.000+00:00\''::timestamp
 \set endDate   '\'2010-11-08T00:00:00.000+00:00\''::timestamp
 \set country1  '\'Ethiopia\''
 \set country2  '\'Belarus\''
 */
SELECT
   co.pl_name AS "country_name",
   extract(
      MONTH
      FROM
         p.m_creationdate
   ) AS messageMonth,
   cr.p_gender AS "person_gender",
   floor(
      extract(
         YEARS
         FROM
            age('2013-01-01' :: date, cr.p_birthday)
      ) / 5
   ) AS ageGroup,
   t.t_name AS "tag_name",
   count(*) AS messageCount
FROM
   message p,
   message_tag pt,
   tag t,
   person cr -- creator
,
   place ci -- city
,
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