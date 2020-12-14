SELECT
  t_name,
  count(*)
FROM
  tag,
  message_tag,
  message,
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
  ) f
WHERE
  m_creatorid = f.k_person2id
  AND m_c_replyof IS NULL
  AND -- post, not comment
  m_messageid = mt_messageid
  AND mt_tagid = t_tagid
  AND t_name <> 'Abbas_I_of_Persia'
  AND EXISTS (
    SELECT
      *
    FROM
      tag,
      message_tag
    WHERE
      mt_messageid = m_messageid
      AND mt_tagid = t_tagid
      AND t_name = 'Abbas_I_of_Persia'
  )
GROUP BY
  t_name
ORDER BY
  2 DESC,
  t_name
LIMIT
  10