SELECT
    p_personid,
    p_firstname,
    p_lastname,
    m_messageid,
    COALESCE(m_ps_imagefile, m_content, ''),
    m_creationdate
FROM
    person,
    message,
    knows
WHERE
    p_personid = m_creatorid
    AND m_creationdate <= '2010-12-01T00:00:00.000+00:00' :: timestamp
    AND k_person1id = 933
    AND k_person2id = p_personid
ORDER BY
    m_creationdate DESC,
    m_messageid ASC
LIMIT
    20;