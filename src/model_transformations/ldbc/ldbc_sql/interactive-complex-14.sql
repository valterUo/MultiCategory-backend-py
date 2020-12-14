WITH start_node(v) AS (
	SELECT
		28587302322727 :: bigint
)
SELECT
	*
FROM
	(
		WITH RECURSIVE search_graph(link, depth, path) AS (
			(
				SELECT
					v :: bigint,
					0,
					ARRAY [] :: bigint [] []
				FROM
					start_node
			)
			UNION
			ALL (
				WITH sg(link, depth) AS (
					SELECT
						*
					FROM
						search_graph
				)
				SELECT
					DISTINCT k_person2id,
					x.depth + 1,
					path || ARRAY [[x.link, k_person2id]]
	        FROM knows, sg x
	        WHERE x.link = k_person1id AND NOT EXISTS(SELECT * FROM sg y WHERE y.link = 933::bigint) AND NOT EXISTS( SELECT * FROM sg y WHERE y.link=k_person2id)
	        )
	),
	paths(pid,path) AS (
		SELECT row_number() OVER (), path FROM search_graph WHERE link = 933::bigint
	),
	edges(id,e) AS (
		SELECT pid, array_agg(path[d1] [d2]
			)
			FROM
				paths,
				generate_subscripts(path, 1) d1,
				generate_subscripts(path, 2) d2
			GROUP BY
				pid,
				d1
		),
		unique_edges(e) AS (
			SELECT
				DISTINCT e
			FROM
				edges
		),
		weights(we, score) AS (
			SELECT
				e,
				sum(score)
			FROM
				(
					SELECT
						e,
						pid1,
						pid2,
						max(score) AS score
					FROM
						(
							SELECT
								e,
								1 AS score,
								p1.m_messageid AS pid1,
								p2.m_messageid AS pid2
							FROM
								edges,
								message p1,
								message p2
							WHERE
								(
									p1.m_creatorid = e [1]
									AND p2.m_creatorid = e [2]
									AND p2.m_c_replyof = p1.m_messageid
									AND p1.m_c_replyof IS NULL
								)
							UNION
							ALL
							SELECT
								e,
								1 AS score,
								p1.m_messageid AS pid1,
								p2.m_messageid AS pid2
							FROM
								edges,
								message p1,
								message p2
							WHERE
								(
									p1.m_creatorid = e [2]
									AND p2.m_creatorid = e [1]
									AND p2.m_c_replyof = p1.m_messageid
									AND p1.m_c_replyof IS NULL
								)
							UNION
							ALL
							SELECT
								e,
								0.5 AS score,
								p1.m_messageid AS pid1,
								p2.m_messageid AS pid2
							FROM
								edges,
								message p1,
								message p2
							WHERE
								(
									p1.m_creatorid = e [1]
									AND p2.m_creatorid = e [2]
									AND p2.m_c_replyof = p1.m_messageid
									AND p1.m_c_replyof IS NOT NULL
								)
							UNION
							ALL
							SELECT
								e,
								0.5 AS score,
								p1.m_messageid AS pid1,
								p2.m_messageid AS pid2
							FROM
								edges,
								message p1,
								message p2
							WHERE
								(
									p1.m_creatorid = e [2]
									AND p2.m_creatorid = e [1]
									AND p2.m_c_replyof = p1.m_messageid
									AND p1.m_c_replyof IS NOT NULL
								)
						) pps
					GROUP BY
						e,
						pid1,
						pid2
				) tmp
			GROUP BY
				e
		),
		weightedpaths(path, score) AS (
			SELECT
				path,
				coalesce(sum(score), 0)
			FROM
				paths,
				edges
				LEFT JOIN weights ON we = e
			WHERE
				pid = id
			GROUP BY
				id,
				path
		)
		SELECT
			path,
			score
		FROM
			weightedpaths
		ORDER BY
			score DESC
	) x
ORDER BY
	score DESC;