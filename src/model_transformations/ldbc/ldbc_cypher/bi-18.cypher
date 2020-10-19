// Q18. Friend recommendation
/*
  :param [{person1Id, tag}] => {RETURN 290 AS person1Id, 'Elizabeth_Taylor' AS tag}
*/
MATCH (person1:Person {id: $person1Id})-[:KNOWS]-(mutualFriend:Person)-[:KNOWS]-(person2:Person)-[:HAS_INTEREST]-(q:Tag {name: $tag})
WHERE person1 <> person2
  AND NOT (person1)-[:KNOWS]-(person2)
RETURN person2.id AS person2Id, count(DISTINCT mutualFriend) AS mutualFriendCount
ORDER BY mutualFriendCount DESC, person2Id ASC
LIMIT 20
