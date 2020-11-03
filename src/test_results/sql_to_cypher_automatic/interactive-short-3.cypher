MATCH (knows : knows) -[k_person2id_p_personid]-> (person : person)
WHERE knows.k_person1id =:personid
RETURN person.p_personid AS p_personid, person.p_firstname AS p_firstname, person.p_lastname AS p_lastname, knows.k_creationdate AS k_creationdate
ORDER BY k_creationdate desc, p_personid asc