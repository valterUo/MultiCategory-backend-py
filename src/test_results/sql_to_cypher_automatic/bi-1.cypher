MATCH (message)
WHERE 1=1 AND 
datetime(message.m_creationdate)<:date
WITH count(*) AS nwo
WITH collect({ cnt : 0.0 + nwo}) AS message_count

MATCH (message)
WHERE 1=1 AND 
datetime(message.m_creationdate)<:date AND 
message.m_ps_imagefile is null
WITH message_count, message
WITH message_count, collect({ messageyear : datetime(message.m_creationdate).year, iscomment : message.m_c_replyof is not null, lengthcategory : case when message.m_length < 40 then 0 when message.m_length < 80 then 1 when message.m_length < 160 then 2 else 3 end, length : message.m_length}) AS message_prep

UNWIND message_prep AS mp
UNWIND message_count AS mc
WITH mp, mc
RETURN mp.messageyear AS messageyear, mp.iscomment AS iscomment, mp.lengthcategory AS lengthcategory, count(*) AS messagecount, avg(mp.length) AS averagemessagelength, sum(mp.length) AS summessagelength, count(*) / mc.cnt AS percentageofmessages
ORDER BY messageyear desc, iscomment asc, lengthcategory asc