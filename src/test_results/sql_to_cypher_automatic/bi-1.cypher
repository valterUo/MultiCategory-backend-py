MATCH (me : message)
WHERE 1= 1
AND datetime(me.m_creationdate) < datetime('2011-07-21T22:00:00.000+00:00')
WITH *, 0.0 + count(*) AS c0
WITH *, collect({cnt : c0}) AS message_count

MATCH (me : message)
WHERE 1= 1
AND datetime(me.m_creationdate) < datetime('2011-07-21T22:00:00.000+00:00')
AND me.m_ps_imagefile IS NULL
WITH *, collect({messageyear : datetime(me.m_creationdate).year, lengthcategory : CASE
WHEN me.m_length < 40 THEN 0
WHEN me.m_length < 80 THEN 1
WHEN me.m_length < 160 THEN 2
ELSE 3
END, m_length : me.m_length}) AS message_prep

UNWIND message_prep AS x1
UNWIND message_count AS mc
WITH *, count(*) AS c3
WITH *, avg(x1.m_length) AS a4
WITH *, sum(x1.m_length) AS s5
WITH *, count(*) / mc.cnt AS c0
RETURN x1.messageyear, x1.iscomment, x1.lengthcategory, c3 AS messagecount, a4 AS averagemessagelength, s5 AS summessagelength, c0 AS percentageofmessages
ORDER BY x1.messageyear, x1.iscomment, x1.lengthcategory