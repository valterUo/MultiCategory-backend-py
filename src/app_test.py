
from model_transformations.query_transformations.parse_tree_trasformations.sql_to_cypher import SqlToCypher
from model_transformations.query_transformations.pgSQL.pgSQL import pgSQL
import json
import os
import glob

query = """
WITH message_count AS (
  SELECT
    0.0 + count(*) AS cnt
  FROM
    message
  WHERE
    1 = 1
    AND m_creationdate < '2011-07-21T22:00:00.000+00:00' :: timestamp
),
message_prep AS (
  SELECT
    extract(
      year
      FROM
        m_creationdate
    ) AS messageYear,
    m_c_replyof IS NOT NULL AS isComment,
    CASE
      WHEN m_length < 40 THEN 0
      WHEN m_length < 80 THEN 1
      WHEN m_length < 160 THEN 2
      ELSE 3
    END AS lengthCategory,
    m_length
  FROM
    message
  WHERE
    1 = 1
    AND m_creationdate < '2011-07-21T22:00:00.000+00:00' :: timestamp
    AND m_ps_imagefile IS NULL
)
SELECT
  messageYear,
  isComment,
  lengthCategory,
  count(*) AS messageCount,
  avg(m_length) AS averageMessageLength,
  sum(m_length) AS sumMessageLength,
  count(*) / mc.cnt AS percentageOfMessages
FROM
  message_prep,
  message_count mc
GROUP BY
  messageYear,
  isComment,
  lengthCategory,
  mc.cnt
ORDER BY
  messageYear DESC,
  isComment ASC,
  lengthCategory ASC;
"""

parse_tree = pgSQL(query).get_parse_tree()

res = SqlToCypher(parse_tree).transform_into_cypher()
print(res)

# with open("C://Users//Valter Uotila//Desktop//NLP//test4.json", "w+") as json_file:
#     json.dump(parse_tree, json_file)

# dirname = os.path.dirname(__file__)
# example_files_path = os.path.join(dirname, "model_transformations//ldbc//ldbc_sql//*.sql")
# example_filenames = glob.glob(example_files_path)
# for file_name in example_filenames:
#       print(file_name)
#       with open(file_name, 'r') as reader:
#             lines = reader.read()
#             parse_tree = pgSQL(lines).get_parse_tree()
#             print(len(parse_tree))
#             with open("C://Users//Valter Uotila//Desktop//parsed_ldbc_queries//" + os.path.basename(file_name) + ".json", "w+") as json_file:
#                   json.dump(parse_tree, json_file)
