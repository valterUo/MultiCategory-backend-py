from model_transformations.query_language_transformations.SQL.sql import SQL
import re
from collections import OrderedDict

# with recursive cposts(m_messageid, m_content, m_ps_imagefile, m_creationdate, m_c_replyof, m_creatorid) AS (
# 	  select m_messageid, m_content, m_ps_imagefile, m_creationdate, m_c_replyof, m_creatorid
# 	  from message
# 	  where m_creatorid = :personId
# 	  order by m_creationdate desc
# 	  limit 10
# ), parent(postid,replyof,orig_postid,creator) AS (
# 	  select m_messageid, m_c_replyof, m_messageid, m_creatorid from cposts
# 	UNION ALL
# 	  select m_messageid, m_c_replyof, orig_postid, m_creatorid
#       from message,parent
#       where m_messageid=replyof
# )
# select p1.m_messageid, COALESCE(m_ps_imagefile,'')||COALESCE(m_content,''), p1.m_creationdate,
#        p2.m_messageid, p2.p_personid, p2.p_firstname, p2.p_lastname
# from
#      (select m_messageid, m_content, m_ps_imagefile, m_creationdate, m_c_replyof from cposts
#      ) p1
#      left join
#      (select orig_postid, postid as m_messageid, p_personid, p_firstname, p_lastname
#       from parent, person
#       where replyof is null and creator = p_personid
#      )p2
#      on p2.orig_postid = p1.m_messageid
#       order by m_creationdate desc, p2.m_messageid desc;


class RECURSIVE_CTE:

    def __init__(self, query_string, rel_db):
        self.query_string = query_string
        self.db = rel_db
        self.recursive_cte_string = None
        self.main_string = None
        self.cte = self.match_names_attributes_blocks()
        for key in self.cte:
            self.cte[key]["query_string"] = process_cte_queries(
                self.cte[key]["query"])
            print("query ", self.cte[key]["query_string"])
            print()
        self.cypher_query = self.transform()

    def get_cypher(self):
        return self.cypher_query

    def match_names_attributes_blocks(self):
        res = re.split(r'\s+|(?=,)|(?=\()|(?=\))', self.query_string)
        res = clean(res)
        collecting_attributes, collecting_query, collecting_main = False, False, False
        cte = OrderedDict()
        cte_name = ""
        paranthesis = []
        for i, elem in enumerate(res):
            #print(elem, cte_name)
            if "(" in elem:
                paranthesis.append("(")
            elif ")" in elem:
                paranthesis.pop()
            if res[i-2] == "with" and res[i-1] == "recursive":
                collecting_attributes = True
                cte_name = elem
                cte[cte_name] = dict()
                cte[cte_name]["attributes"], cte[cte_name]["query"] = [], []
                cte[cte_name]["recursive"] = False
            elif collecting_attributes and elem == ")" and res[i+1] == "AS" and res[i+2] == "(" and len(paranthesis) == 0:
                collecting_attributes = False
                collecting_query = True
            elif elem == ")" and res[i+1] == "select" and len(paranthesis) == 0:
                collecting_query = False
                collecting_main = True
                cte["main"] = dict()
                cte["main"]["query"] = list()
            elif elem == ")" and len(paranthesis) == 0 and not collecting_main:
                collecting_attributes = True
                collecting_query = False
                cte_name = res[i+1]
                cte[cte_name] = dict()
                cte[cte_name]["attributes"], cte[cte_name]["query"] = [], []
                cte[cte_name]["recursive"] = False
            if collecting_attributes:
                if elem != cte_name:
                    cte[cte_name]["attributes"].append(
                        elem.replace(")", "").replace("(", ""))
            if collecting_query:
                if elem == cte_name:
                    cte[cte_name]["recursive"] = True
                cte[cte_name]["query"].append(elem)
            if collecting_main:
                cte["main"]["query"].append(elem)
        return cte

    def transform(self):
        return self.transform_recursive_cte_to_cypher()

    def transform_recursive_cte_to_cypher(self):
        query = ""
        for key in self.cte:
            if key != 'main':
                if self.cte[key]["recursive"]:
                    query += self.parse_recursive_cte(self.cte[key]["query"])
                else:
                    res = SQL(
                        key, self.cte[key]["query_string"], self.db, main_block=False)
                    query += res.get_cypher()
            else:
                # print()
                # print(self.cte["main"]["query_string"])
                # print()
                # res = SQL(key, self.cte["main"]["query_string"], self.db)
                # query += res.get_cypher()
                query = query
        return query

    def parse_recursive_cte(self, orig_query):
        union_index = orig_query.index("UNION")
        before_union = orig_query[:union_index]
        after_union = orig_query[union_index:]
        if after_union[0] == "UNION" and after_union[1] == "ALL":
            after_union = after_union[2:]
        elif after_union[0] == "UNION":
            after_union = after_union[1:]
        if before_union[0] == ")" and before_union[1] == "AS" and before_union[2] == "(":
            before_union = before_union[3:]
        elif before_union[0] == "(":
            before_union = before_union[1:]
        print("Before: ", before_union)
        print("After union: ", after_union)
        query = ""
        print(orig_query)
        initial_node = ""
        #if self.db.contains_table()
        return query


def clean(l):
    r = []
    for e in l:
        e = e.strip()
        if e != None and e != "":
            r.append(e)
    return r


def process_cte_queries(query_list):
    result = ""
    start = False
    for elem in query_list:
        if start:
            if elem == ",":
                result += elem
            else:
                result += elem + " "
        if elem == "select" and not start:
            start = True
            result += elem + " "
    return result
