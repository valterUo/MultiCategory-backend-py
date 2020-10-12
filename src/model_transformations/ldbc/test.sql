-- Populate forum table
--\copy forum FROM 'C:/Users/Valter Uotila/Desktop/ldbc_snb_implementations/postgres/test-data/dynamic/forum_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate forum_person table
\copy forum_person FROM 'C:/Users/Valter Uotila/Desktop/ldbc_snb_implementations/postgres/test-data/dynamic/forum_hasMember_person_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate forum_tag table
\copy forum_tag FROM 'C:/Users/Valter Uotila/Desktop/ldbc_snb_implementations/postgres/test-data/dynamic/forum_hasTag_tag_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate organisation table
\copy organisation FROM 'C:/Users/Valter Uotila/Desktop/ldbc_snb_implementations/postgres/test-data/static/organisation_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate person table
\copy person FROM 'C:/Users/Valter Uotila/Desktop/ldbc_snb_implementations/postgres/test-data/dynamic/person_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate person_email table
\copy person_email FROM 'C:/Users/Valter Uotila/Desktop/ldbc_snb_implementations/postgres/test-data/dynamic/person_email_emailaddress_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate person_tag table
\copy person_tag FROM 'C:/Users/Valter Uotila/Desktop/ldbc_snb_implementations/postgres/test-data/dynamic/person_hasInterest_tag_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate knows table
\copy knows ( k_creationdate, k_deletiondate, k_person1id, k_person2id) FROM 'C:/Users/Valter Uotila/Desktop/ldbc_snb_implementations/postgres/test-data/dynamic/person_knows_person_0_0.csv' WITH DELIMITER '|' CSV HEADER;
\copy knows ( k_creationdate, k_deletiondate, k_person2id, k_person1id) FROM 'C:/Users/Valter Uotila/Desktop/ldbc_snb_implementations/postgres/test-data/dynamic/person_knows_person_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate likes table
\copy likes FROM 'C:/Users/Valter Uotila/Desktop/ldbc_snb_implementations/postgres/test-data/dynamic/person_likes_post_0_0.csv' WITH DELIMITER '|' CSV HEADER;
\copy likes FROM 'C:/Users/Valter Uotila/Desktop/ldbc_snb_implementations/postgres/test-data/dynamic/person_likes_comment_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate person_language table
\copy person_language FROM 'C:/Users/Valter Uotila/Desktop/ldbc_snb_implementations/postgres/test-data/dynamic/person_speaks_language_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate person_university table
\copy person_university FROM 'C:/Users/Valter Uotila/Desktop/ldbc_snb_implementations/postgres/test-data/dynamic/person_studyAt_organisation_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate person_company table
\copy person_company FROM 'C:/Users/Valter Uotila/Desktop/ldbc_snb_implementations/postgres/test-data/dynamic/person_workAt_organisation_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate place table
\copy place FROM 'C:/Users/Valter Uotila/Desktop/ldbc_snb_implementations/postgres/test-data/static/place_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate message_tag table
\copy message_tag FROM 'C:/Users/Valter Uotila/Desktop/ldbc_snb_implementations/postgres/test-data/dynamic/post_hasTag_tag_0_0.csv' WITH DELIMITER '|' CSV HEADER;
\copy message_tag FROM 'C:/Users/Valter Uotila/Desktop/ldbc_snb_implementations/postgres/test-data/dynamic/comment_hasTag_tag_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate tagclass table
\copy tagclass FROM 'C:/Users/Valter Uotila/Desktop/ldbc_snb_implementations/postgres/test-data/static/tagclass_0_0.csv' WITH DELIMITER '|' CSV HEADER;

-- Populate tag table
\copy tag FROM 'C:/Users/Valter Uotila/Desktop/ldbc_snb_implementations/postgres/test-data/static/tag_0_0.csv' WITH DELIMITER '|' CSV HEADER;


-- PROBLEMATIC

-- Populate message table
\copy message (m_creationdate, m_deletiondate, m_messageid, m_ps_imagefile, m_locationip, m_browserused, m_ps_language, m_content, m_length, m_creatorid, m_ps_forumid, m_locationid) FROM 'C:/Users/Valter Uotila/Desktop/ldbc_snb_implementations/postgres/test-data/dynamic/post_0_0.csv' WITH (FORCE_NOT_NULL ("m_content"),  DELIMITER '|', HEADER, FORMAT csv);
\copy message (m_creationdate, m_deletiondate, m_messageid, m_locationip, m_browserused, m_content, m_length, m_creatorid, m_locationid, m_c_replyof) FROM 'C:/Users/Valter Uotila/Desktop/ldbc_snb_implementations/postgres/test-data/dynamic/comment_0_0.csv' WITH (FORCE_NOT_NULL ("m_content"),  DELIMITER '|', HEADER, FORMAT csv);

create view country as select city.pl_placeid as ctry_city, ctry.pl_name as ctry_name from place city, place ctry where city.pl_containerplaceid = ctry.pl_placeid and ctry.pl_type = 'country';

vacuum analyze;