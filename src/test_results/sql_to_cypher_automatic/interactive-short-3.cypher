MATCH (knows : knows) -[k_person2id_p_personid]-> (person : person)
WHERE knows.k_person1id =:personid
RETURN person.p_personid AS personid, person.p_firstname AS firstname, person.p_lastname AS lastname, knows.k_creationdate AS creationdate
ORDER BY creationdate desc,personid asc