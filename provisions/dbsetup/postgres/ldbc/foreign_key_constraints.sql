-- We need to input fk pk constraints implicitly
-- This file is not part of the original LDBC benchmark

ALTER TABLE forum ADD FOREIGN KEY (f_moderatorid) REFERENCES person (p_personid);
ALTER TABLE forum_person ADD FOREIGN KEY (fp_forumid) REFERENCES forum (f_forumid);
ALTER TABLE forum_person ADD FOREIGN KEY (fp_personid) REFERENCES person (p_personid);
ALTER TABLE forum_tag ADD FOREIGN KEY (ft_forumid) REFERENCES forum (f_forumid);
ALTER TABLE forum_tag ADD FOREIGN KEY (ft_tagid) REFERENCES tag (t_tagid);
ALTER TABLE knows ADD FOREIGN KEY (k_person1id) REFERENCES person (p_personid);
ALTER TABLE knows ADD FOREIGN KEY (k_person2id) REFERENCES person (p_personid);
ALTER TABLE likes ADD FOREIGN KEY (l_personid) REFERENCES person (p_personid);
ALTER TABLE likes ADD FOREIGN KEY (l_messageid) REFERENCES message (m_messageid);
ALTER TABLE organisation ADD FOREIGN KEY (o_placeid) REFERENCES place (pl_placeid);
ALTER TABLE person ADD FOREIGN KEY (p_placeid) REFERENCES place (pl_placeid);
ALTER TABLE person_company ADD FOREIGN KEY (pc_personid) REFERENCES person (p_personid);
ALTER TABLE person_company ADD FOREIGN KEY (pc_organisationid) REFERENCES organisation (o_organisationid);
ALTER TABLE person_email ADD FOREIGN KEY (pe_personid) REFERENCES person (p_personid);
ALTER TABLE person_language ADD FOREIGN KEY (plang_personid) REFERENCES person (p_personid);
ALTER TABLE person_tag ADD FOREIGN KEY (pt_personid) REFERENCES person (p_personid);
ALTER TABLE person_tag ADD FOREIGN KEY (pt_tagid) REFERENCES tag (t_tagid);
ALTER TABLE person_university ADD FOREIGN KEY (pu_personid) REFERENCES person (p_personid);
ALTER TABLE person_university ADD FOREIGN KEY (pu_organisationid) REFERENCES organisation (o_organisationid);
ALTER TABLE message_tag ADD FOREIGN KEY (mt_messageid) REFERENCES message (m_messageid);
ALTER TABLE message_tag ADD FOREIGN KEY (mt_tagid) REFERENCES tag (t_tagid);
ALTER TABLE tag ADD FOREIGN KEY (t_tagclassid) REFERENCES tagclass (tc_tagclassid);
ALTER TABLE tagclass ADD FOREIGN KEY (tc_subclassoftagclassid) REFERENCES tagclass (tc_tagclassid);
ALTER TABLE message ADD FOREIGN KEY (m_creatorid) REFERENCES person (p_personid);
ALTER TABLE message ADD FOREIGN KEY (m_locationid) REFERENCES place (pl_placeid);

--ALTER TABLE message ADD FOREIGN KEY (m_ps_forumid) REFERENCES forum (f_forumid);
--ALTER TABLE place ADD FOREIGN KEY (pl_containerplaceid) REFERENCES person (p_personid);

-- The following is important for path queries
--ALTER TABLE message ADD FOREIGN KEY (m_c_replyof) REFERENCES message (m_messageid);