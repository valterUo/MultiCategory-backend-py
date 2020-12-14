SELECT
    COALESCE(m_ps_imagefile, '') || COALESCE(m_content, ''),
    m_creationdate
FROM
    message
WHERE
    m_messageid = 618475290635;