SELECT
      t_name,
      count(*)
FROM
      tag,
      message,
      message_tag recent,
      knows
WHERE
      m_messageid = mt_messageid
      AND mt_tagid = t_tagid
      AND m_creatorid = k_person2id
      AND m_c_replyof IS NULL
      AND -- post, not comment
      k_person1id = 933
      AND m_creationdate >= '2010-11-01T00:00:00.000+00:00' :: timestamp
      AND m_creationdate < (
            '2010-11-01T00:00:00.000+00:00' :: timestamp + INTERVAL '1 days' * 20
      )
      AND NOT EXISTS (
            SELECT
                  *
            FROM
                  (
                        SELECT
                              DISTINCT mt_tagid
                        FROM
                              message,
                              message_tag,
                              knows
                        WHERE
                              k_person1id = 933
                              AND k_person2id = m_creatorid
                              AND m_c_replyof IS NULL
                              AND -- post, not comment
                              mt_messageid = m_messageid
                              AND m_creationdate < '2008-11-01T00:00:00.000+00:00' :: timestamp
                  ) tags
            WHERE
                  tags.mt_tagid = recent.mt_tagid
      )
GROUP BY
      t_name
ORDER BY
      2 DESC,
      t_name
LIMIT
      10