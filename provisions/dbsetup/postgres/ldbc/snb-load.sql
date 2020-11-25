-- Populate forum table
\copy forum FROM 'ldbc_flatfiles/forum_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate forum_person table
\copy forum_person FROM 'ldbc_flatfiles/forum_hasMember_person_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate forum_tag table
\copy forum_tag FROM 'ldbc_flatfiles/forum_hasTag_tag_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate organisation table
\copy organisation FROM 'ldbc_flatfiles/organisation_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate person table
\copy person FROM 'ldbc_flatfiles/person_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate person_email table
\copy person_email FROM 'ldbc_flatfiles/person_email_emailaddress_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate person_tag table
\copy person_tag FROM 'ldbc_flatfiles/person_hasInterest_tag_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate knows table
\copy knows ( k_creationdate, k_deletiondate, k_person1id, k_person2id) FROM 'ldbc_flatfiles/person_knows_person_0_0.csv' WITH DELIMITER '|' CSV HEADER;
\copy knows ( k_creationdate, k_deletiondate, k_person2id, k_person1id) FROM 'ldbc_flatfiles/person_knows_person_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate likes table
\copy likes FROM 'ldbc_flatfiles/person_likes_post_0_0.csv' WITH DELIMITER '|' CSV HEADER;
\copy likes FROM 'ldbc_flatfiles/person_likes_comment_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate person_language table
\copy person_language FROM 'ldbc_flatfiles/person_speaks_language_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate person_university table
\copy person_university FROM 'ldbc_flatfiles/person_studyAt_organisation_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate person_company table
\copy person_company FROM 'ldbc_flatfiles/person_workAt_organisation_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate place table
\copy place FROM 'ldbc_flatfiles/place_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate message_tag table
\copy message_tag FROM 'ldbc_flatfiles/post_hasTag_tag_0_0.csv' WITH DELIMITER '|' CSV HEADER;
\copy message_tag FROM 'ldbc_flatfiles/comment_hasTag_tag_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate tagclass table
\copy tagclass FROM 'ldbc_flatfiles/tagclass_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate tag table
\copy tag FROM 'ldbc_flatfiles/tag_0_0.csv' WITH DELIMITER '|' CSV HEADER;


-- PROBLEMATIC

-- Populate message table
-- \copy message FROM 'ldbc_flatfiles/post_0_0-postgres.csv'    WITH (FORCE_NOT_NULL ("m_content"),  DELIMITER '|', HEADER, FORMAT csv);
-- \copy message FROM 'ldbc_flatfiles/comment_0_0-postgres.csv' WITH (FORCE_NOT_NULL ("m_content"),  DELIMITER '|', HEADER, FORMAT csv);

-- create view country as select city.pl_placeid as ctry_city, ctry.pl_name as ctry_name from place city, place ctry where city.pl_containerplaceid = ctry.pl_placeid and ctry.pl_type = 'country';

-- vacuum analyze;
