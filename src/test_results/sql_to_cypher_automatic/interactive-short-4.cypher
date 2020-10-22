MATCH (message)
WHERE message.m_messageid =:messageid
RETURN coalesce(message.m_ps_imagefile,'')+coalesce(message.m_content,'') AS ps, message.m_creationdate AS creationdate