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

--ALTER TABLE place ADD FOREIGN KEY (pl_containerplaceid) REFERENCES person (p_personid);

ALTER TABLE message ADD FOREIGN KEY (m_creatorid) REFERENCES person (p_personid);
ALTER TABLE message ADD FOREIGN KEY (m_locationid) REFERENCES place (pl_placeid);
--ALTER TABLE message ADD FOREIGN KEY (m_ps_forumid) REFERENCES forum (f_forumid);
--ALTER TABLE message ADD FOREIGN KEY (m_c_replyof) REFERENCES person (p_personid);

ALTER TABLE message_tag ADD FOREIGN KEY (mt_messageid) REFERENCES message (m_messageid);
ALTER TABLE message_tag ADD FOREIGN KEY (mt_tagid) REFERENCES tag (t_tagid);

ALTER TABLE tag ADD FOREIGN KEY (t_tagclassid) REFERENCES tagclass (tc_tagclassid);

ALTER TABLE tagclass ADD FOREIGN KEY (tc_subclassoftagclassid) REFERENCES tagclass (tc_tagclassid);

CREATE INDEX forum_moderatorid ON forum (f_moderatorid);

CREATE INDEX forum_person_forumid ON forum_person (fp_forumid);
CREATE INDEX forum_person_personid ON forum_person (fp_personid);

CREATE INDEX forum_tag_forumid ON forum_tag (ft_forumid);

CREATE INDEX forum_tag_tagid ON forum_tag (ft_tagid);

CREATE INDEX knows_person1id ON knows (k_person1id);
CREATE INDEX knows_person2id ON knows (k_person2id);

CREATE INDEX likes_personid ON likes (l_personid);
CREATE INDEX likes_messageid ON likes (l_messageid);

CREATE INDEX organisation_placeid ON organisation (o_placeid);

CREATE INDEX person_placeid ON person (p_placeid);

CREATE INDEX person_company_personid ON person_company (pc_personid);
CREATE INDEX person_company_organisationid ON person_company (pc_organisationid);

CREATE INDEX person_email_personid ON person_email (pe_personid);
CREATE INDEX person_language_personid ON person_language (plang_personid);
CREATE INDEX person_tag_personid ON person_tag (pt_personid);
CREATE INDEX person_tag_tagid ON person_tag (pt_tagid);
CREATE INDEX person_university_personid ON person_university (pu_personid);
CREATE INDEX person_university_organisationid ON person_university (pu_organisationid);
CREATE INDEX place_containerplaceid ON place (pl_containerplaceid);
CREATE INDEX message_creatorid ON message (m_creatorid);
CREATE INDEX message_locationid ON message (m_locationid);
CREATE INDEX message_forumid ON message (m_ps_forumid);
CREATE INDEX message_replyof ON message (m_c_replyof);
CREATE INDEX message_tag_messageid ON message_tag (mt_messageid);
CREATE INDEX message_tag_tagid ON message_tag (mt_tagid);
CREATE INDEX tag_tagclassid ON tag (t_tagclassid);
CREATE INDEX tagclass_subclassoftagclassid ON tagclass (tc_subclassoftagclassid);