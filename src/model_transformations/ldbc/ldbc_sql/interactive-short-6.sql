WITH RECURSIVE chain(parent, child) AS(
	SELECT
		m_c_replyof,
		m_messageid
	FROM
		message
	WHERE
		m_messageid = 618475290635
	UNION
	ALL
	SELECT
		p.m_c_replyof,
		p.m_messageid
	FROM
		message p,
		chain c
	WHERE
		p.m_messageid = c.parent
)
SELECT
	f_forumid,
	f_title,
	p_personid,
	p_firstname,
	p_lastname
FROM
	message,
	person,
	forum
WHERE
	m_messageid = (
		SELECT
			coalesce(min(parent), 618475290635)
		FROM
			chain
	)
	AND m_ps_forumid = f_forumid
	AND f_moderatorid = p_personid;