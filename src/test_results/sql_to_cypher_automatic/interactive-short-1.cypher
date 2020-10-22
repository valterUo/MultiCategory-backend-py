MATCH (person)
WHERE person.p_personid =:personid
RETURN person.p_firstname AS firstname, person.p_lastname AS lastname, person.p_birthday AS birthday, person.p_locationip AS locationip, person.p_browserused AS browserused, person.p_placeid AS placeid, person.p_gender AS gender, person.p_creationdate AS creationdate