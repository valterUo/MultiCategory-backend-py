SELECT
    p_personid,
    p_firstname,
    p_lastname
FROM
    message,
    person
WHERE
    m_messageid = 618475290635
    AND m_creatorid = 933;