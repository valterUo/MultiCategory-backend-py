MATCH (message: message)
WHERE message.m_messageid = :messageid
RETURN coalesce(message.m_ps_imagefile,'')+coalesce(message.m_content,''), message.m_creationdate AS m_creationdate