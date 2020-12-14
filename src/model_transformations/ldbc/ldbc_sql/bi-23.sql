/* Q23. Holiday destinations
 \set country  '\'Belarus\''
 */
SELECT
   count(*) AS messageCount,
   dest.pl_name AS "destination_name",
   extract(
      MONTH
      FROM
         m.m_creationdate
   ) AS MONTH
FROM
   place pco -- person country
,
   place pci -- person city
,
   person p,
   message m,
   place dest
WHERE
   1 = 1 -- join
   AND pco.pl_placeid = pci.pl_containerplaceid
   AND pci.pl_placeid = p.p_placeid
   AND p.p_personid = m.m_creatorid
   AND m.m_locationid = dest.pl_placeid -- filter
   AND pco.pl_name = 'Belarus'
   AND m.m_locationid != pco.pl_placeid
GROUP BY
   dest.pl_name,
   MONTH
ORDER BY
   messageCount DESC,
   dest.pl_name,
   MONTH
LIMIT
   100;