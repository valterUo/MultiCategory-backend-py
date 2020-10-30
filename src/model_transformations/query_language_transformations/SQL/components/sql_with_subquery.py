import re
import itertools
from collections import OrderedDict
from model_transformations.query_language_transformations.SQL.independent_sql_parsing_tools import *


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

class SQL_with_subquery:

    def __init__(self, name, whole_query, rel_db):
        self.name = name
        self.whole_query = whole_query
        self.rel_db = rel_db
        self.query = self.parse_subqueries()
        for key in self.query:
            for key2 in self.query[key]:
                self.query[key][key2] = clean(self.query[key][key2])
            print(key)
            print(self.query[key])
            print()
        self.cypher_query = ""

    def parse_subqueries(self):
        words = clean(re.split(r'\s|(?=\()|(?<=\()|(?=\))|(?<=\))', self.whole_query))
        query = OrderedDict()
        select_indices = [i for i, x in enumerate(words) if x == "select"]
        print(select_indices)
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
                    check = word.replace(")", "").replace("(", "").replace(",", "").strip()
                    if check in KEYWORDS and len(paranthesis) == 0:
                        current_keyword = check
                        current_dict[current_keyword] = []
                        continue
                    current_dict[current_keyword].append(word)
                    if i == len(words) - 1:
                        query["main"] = current_dict
                        current_dict = dict()
            
        return query

    def get_cypher(self):
        return self.cypher_query