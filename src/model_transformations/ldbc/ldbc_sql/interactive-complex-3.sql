SELECT
  p_personid,
  p_firstname,
  p_lastname,
  ct1,
  ct2,
  total
FROM
  (
    SELECT
      k_person2id
    FROM
      knows
    WHERE
      k_person1id = 28587302322727
    UNION
    SELECT
      k2.k_person2id
    FROM
      knows k1,
      knows k2
    WHERE
      k1.k_person1id = 28587302322727
      AND k1.k_person2id = k2.k_person1id
      AND k2.k_person2id <> 28587302322727
  ) f,
  person,
  place p1,
  place p2,
  (
    SELECT
      chn.m_c_creatorid,
      ct1,
      ct2,
      ct1 + ct2 AS total
    FROM
      (
        SELECT
          m_creatorid AS m_c_creatorid,
          count(*) AS ct1
        FROM
          message,
          place
        WHERE
          m_locationid = pl_placeid
          AND pl_name = 'Belarus'
          AND m_creationdate >= '2010-11-01T00:00:00.000+00:00' :: timestamp
          AND m_creationdate < (
            '2010-11-01T00:00:00.000+00:00' :: timestamp + INTERVAL '1 days' * 20
          )
        GROUP BY
          m_c_creatorid
      ) chn,
      (
        SELECT
          m_creatorid AS m_c_creatorid,
          count(*) AS ct2
        FROM
          message,
          place
        WHERE
          m_locationid = pl_placeid
          AND pl_name = 'India'
          AND m_creationdate >= '2010-11-01T00:00:00.000+00:00' :: timestamp
          AND m_creationdate < (
            '2010-11-01T00:00:00.000+00:00' :: timestamp + INTERVAL '1 days' * 20
          )
        GROUP BY
          m_creatorid --m_c_creatorid
      ) ind
    WHERE
      CHN.m_c_creatorid = IND.m_c_creatorid
  ) cpc
WHERE
  f.k_person2id = p_personid
  AND p_placeid = p1.pl_placeid
  AND p1.pl_containerplaceid = p2.pl_placeid
  AND p2.pl_name <> 'Belarus'
  AND p2.pl_name <> 'India'
  AND f.k_person2id = cpc.m_c_creatorid
ORDER BY
  6 DESC,
  1
LIMIT
  20