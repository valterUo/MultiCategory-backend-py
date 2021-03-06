/* Q13. Popular Tags per month in a country
 \set country  '\'Belarus\''
 */
WITH detail AS (
     SELECT
          extract(
               YEAR
               FROM
                    m.m_creationdate
          ) AS year,
          extract(
               MONTH
               FROM
                    m.m_creationdate
          ) AS MONTH,
          t.t_name AS tagName,
          count(DISTINCT m.m_messageid) AS popularity,
          row_number() OVER (
               PARTITION BY extract(
                    YEAR
                    FROM
                         m.m_creationdate
               ),
               extract(
                    MONTH
                    FROM
                         m.m_creationdate
               )
               ORDER BY
                    t.t_name IS NULL -- sort order is: false, true i.e. first the given, then missing tags
,
                    count(DISTINCT m.m_messageid) DESC,
                    t.t_name
          ) AS rn
     FROM
          place c -- country
,
          message m
          LEFT JOIN message_tag pt ON (m.m_messageid = pt.mt_messageid)
          LEFT JOIN tag t ON (pt.mt_tagid = t.t_tagid)
     WHERE
          1 = 1 -- join
          AND c.pl_placeid = m.m_locationid -- filter
          AND c.pl_name = 'Belarus'
     GROUP BY
          year,
          MONTH,
          t.t_name
)
SELECT
     year,
     MONTH,
     CASE
          WHEN count(tagName) = 0 THEN ARRAY [] :: varchar [] [] -- for the given month, no messages have any tags, so we return an empty array
          -- we have non-missing tags, and also the missing tag might show up, so we filter it out
          ELSE array_agg(
               ARRAY [tagName, cast(popularity AS VARCHAR)]
               ORDER BY
                    popularity DESC,
                    tagName
          ) FILTER (
               WHERE
                    tagName IS NOT NULL
          )
     END AS popularTags
FROM
     detail
WHERE
     rn <= 5
GROUP BY
     year,
     MONTH
ORDER BY
     year DESC,
     MONTH
LIMIT
     100;