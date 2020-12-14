WITH RECURSIVE search_graph(link, depth) AS (
	SELECT
		28587302322727 :: bigint,
		0
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
			x.depth + 1
		FROM
			knows,
			sg x
		WHERE
			x.link = k_person1id
			AND NOT EXISTS(
				SELECT
					*
				FROM
					sg y
				WHERE
					y.link = 933 :: bigint
			)
			AND NOT EXISTS(
				SELECT
					*
				FROM
					sg y
				WHERE
					y.link = k_person2id
			)
	)
)
SELECT
	max(depth)
FROM
	(
		SELECT
			depth
		FROM
			search_graph
		WHERE
			link = 933 :: bigint
		UNION
		SELECT
			-1
	) tmp;