import re
from collections import OrderedDict

from model_transformations.query_transformations.SQL.independent_sql_parsing_tools import *
from model_transformations.query_transformations.SQL.sql import SQL


## SQL query that contains subqueries but no ctes

# select p1.m_messageid, COALESCE(m_ps_imagefile,'')||COALESCE(m_content,''), p1.m_creationdate,
#        p2.m_messageid, p2.p_personid, p2.p_firstname, p2.p_lastname
# from
#      (select m_messageid, m_content, m_ps_imagefile, m_creationdate, m_c_replyof from cposts
#      ) p1
#      left join
#      (select orig_postid, postid as m_messageid, p_personid, p_firstname, p_lastname
#       from parent, person
#       where replyof is null and creator = p_personid
#      ) p2
#      on p2.orig_postid = p1.m_messageid
#       order by m_creationdate desc, p2.m_messageid desc;

# select p1.m_messageid, COALESCE(m_ps_imagefile,'')||COALESCE(m_content,''), p1.m_creationdate,
#        p2.m_messageid, p2.p_personid, p2.p_firstname, p2.p_lastname
# from 
#      p1 left join p2
#      on p2.orig_postid = p1.m_messageid
#       order by m_creationdate desc, p2.m_messageid desc;

# ## First subquery
# UNWIND cposts as var1
# collect({ m_messageid : var1.m_messageid, m_content : var1.m_content, m_ps_imagefile : var1.m_ps_imagefile, m_creationdate : var1.m_creationdate, m_c_replyof : var1.m_c_replyof}) AS p1

# ## Second subquery
# UNWIND parent as var2
# MATCH (p : person)
# WHERE p.p_personid = var2.creator
# AND var2.replyof is null
# collect({var2.orig_postid, m_messageid : var2.postid, p_personid : p_personid, p_firstname : p.p_firstname, p_lastname : p.p_lastname}) AS p2

# ## The main query
# UNWIND p1 AS x
# UNWIND p2 AS y
# WHERE x.m_messageid = y.orig_postid
# RETURN x.m_messageid, COALESCE(x.m_ps_imagefile,'') + COALESCE(x.m_content,''), x.m_creationdate, y.m_messageid, y.p_personid, y.p_firstname, y.p_lastname
# ORDER BY x.m_creationdate desc, y.m_messageid desc


class SQL_with_subquery:

    def __init__(self, name, whole_query, rel_db):
        self.name = name
        self.whole_query = whole_query
        self.rel_db = rel_db
        self.query = self.parse_subqueries()
        for key in self.query:
            for key2 in self.query[key]:
                self.query[key][key2] = clean(self.query[key][key2])
        self.cypher_query = self.transform_into_cypher()

    def parse_subqueries(self):
        words = clean(
            re.split(r'\s|(?=\()|(?<=\()|(?=\))|(?<=\))', self.whole_query))
        query = OrderedDict()
        select_indices = [i for i, x in enumerate(words) if x == "select"]
        current_keyword = None
        for j in select_indices:
            paranthesis = []
            current_dict = dict()
            for i, word in enumerate(words):
                if i >= j:
                    if word == "(":
                        paranthesis.append("(")
                    if word == ")":
                        if len(paranthesis) > 0:
                            paranthesis.pop()
                        elif len(paranthesis) == 0:
                            query[words[i+1]] = current_dict
                            current_dict = dict()
                            break
                    check = word.replace(")", "").replace(
                        "(", "").replace(",", "").strip()
                    if check in KEYWORDS and len(paranthesis) == 0:
                        current_keyword = check
                        current_dict[current_keyword] = []
                        continue
                    current_dict[current_keyword].append(word)
                    if i == len(words) - 1:
                        query["main"] = current_dict
                        current_dict = dict()
        return query

    def transform_into_cypher(self):
        result = ""
        for key in self.query:
            if key != 'main':
                query_string = ""
                for key2 in self.query[key]:
                    query_string += key2 + " " + \
                        " ".join(self.query[key][key2]) + " "
                res = SQL(key, query_string, self.rel_db, main_block=False)
                result += res.get_cypher()
        # query_string = ""
        # for key in self.query["main"]:
        #     query_string += key + " ".join(self.query['main'][key])
        # res = SQL('main', query_string, self.rel_db)
        # result += res.get_cypher()
        return result

    def get_cypher(self):
        return self.cypher_query
