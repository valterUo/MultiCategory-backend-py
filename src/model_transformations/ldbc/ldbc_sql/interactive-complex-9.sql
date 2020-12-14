SELECT
  p_personid,
  p_firstname,
  p_lastname,
  m_messageid,
  COALESCE(m_ps_imagefile, '') || COALESCE(m_content, ''),
  m_creationdate
FROM
  (
    SELECT
      k_person2id
    FROM
      knows
    WHERE
      k_person1id = 933
    UNION
    SELECT
      k2.k_person2id
    FROM
      knows k1,
      knows k2
    WHERE
      k1.k_person1id = 933
      AND k1.k_person2id = k2.k_person1id
      AND k2.k_person2id <> 933
  ) f,
  person,
  message
WHERE
  p_personid = m_creatorid
  AND p_personid = f.k_person2id
  AND m_creationdate < '2010-11-01T00:00:00.000+00:00' :: timestamp
ORDER BY
  m_creationdate DESC,
  m_messageid ASC
LIMIT
  20