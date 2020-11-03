MATCH (message: message)
WHERE 1=1 AND
datetime(message.m_creationdate)<:date
WITH count(*) AS mjm
WITH collect({ cnt : 0.0 + mjm}) AS message_count

MATCH (message: message)
WHERE 1=1 AND
datetime(message.m_creationdate)<:date AND
message.m_ps_imagefile is null
WITH message_count, message
WITH message_count, collect({ messageyear : datetime(message.m_creationdate).year, iscomment : message.m_c_replyof is not null, lengthcategory : case when message.m_length < 40 then 0 when message.m_length < 80 then 1 when message.m_length < 160 then 2 else 3 end, m_length : message.m_length}) AS message_prep

UNWIND message_prep AS yku
UNWIND message_count AS mc
WITH yku, mc
RETURN yku.messageyear AS messageyear, yku.iscomment AS iscomment, yku.lengthcategory AS lengthcategory, count(*) AS messagecount, avg(yku.m_length) AS averagemessagelength, sum(yku.m_length) AS summessagelength, count(*) / mc.cnt AS percentageofmessages
ORDER BY  messageyear desc, iscomment asc, lengthcategory asc