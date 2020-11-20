from model_transformations.query_transformations.SQL.independent_sql_parsing_tools import clean, get_random_string
from model_transformations.query_transformations.SQL.sql import SQL
import re
from collections import OrderedDict
from model_transformations.query_transformations.SQL.global_variables import KEYWORDS

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
#       from message, parent
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
#      ) p2
#      on p2.orig_postid = p1.m_messageid
#       order by m_creationdate desc, p2.m_messageid desc;


class RECURSIVE_CTE:

    def __init__(self, name, query_string, rel_db):
        self.name = name
        self.query_string = query_string
        self.db = rel_db
        self.recursive_cte_string = None
        self.main_string = None
        self.cte = self.match_names_attributes_blocks()
        for key in self.cte:
            self.cte[key]["query_string"] = process_cte_queries(
                self.cte[key]["query"])
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
                cte_name = res[i+2]
                cte[cte_name] = dict()
                cte[cte_name]["attributes"], cte[cte_name]["query"] = [], []
                cte[cte_name]["recursive"] = False
            if collecting_attributes:
                if elem != cte_name:
                    cleaned = elem.replace(")", "").replace(
                        "(", "").replace(",", "")
                    if cleaned != "":
                        cte[cte_name]["attributes"].append(cleaned)
            if collecting_query:
                elem = elem.strip()
                if elem.replace(",", "") == cte_name:
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
                    query += self.parse_recursive_cte(key,
                                                      self.cte[key]["query"])
                else:
                    #print(self.cte[key]["query_string"])
                    res = SQL(
                        key, self.cte[key]["query_string"], self.db, main_block=False)
                    query += res.get_cypher()
            else:
                # res = SQL(key, self.cte["main"]["query_string"], self.db)
                # query += res.get_cypher()
                query = query
        return query

    def parse_recursive_cte(self, cte_name, orig_query):
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
        query = ""
        before_union_parsed = self.assign_keyword_parts(cte_name, before_union)
        after_union_parsed = self.assign_keyword_parts(cte_name, after_union)
        #print("Before: ", before_union_parsed)
        # print("After union: ", after_union_parsed)
        initial_node = ""
        unwind_var = get_random_string(3)
        ## Mapping before the union part to cypher
        for col in before_union_parsed["from"]:
            #print(col)
            if self.db.contains_table(col):
                initial_node += "MATCH (" + col + ")\n"
            elif col in self.cte.keys():
                initial_node += "UNWIND " + col + " AS " + unwind_var + "\n"

        ## Mapping after the union part to cypher path expression
        ## The algorithm assumes that the WHERE clause defines edge property in the graph

        ## MATCH (m : message) -[m_c_replyof_m_messageid*0..] -> (n : message)
        ## WITH collect({postid : n.m_messageid, replyof : n.m_c_replyof, orig_postid : m.m_messageid, creator: n.m_creatorid}) as parent
        path_expression = ""
        if len(after_union_parsed["from"]) == 1:
            prop = after_union_parsed["from"][0]

            pk, edge_label = self.parse_edge_label(
                cte_name, before_union_parsed, after_union_parsed)
            pk2 = pk
            if "_" in pk:
                pk2 = pk.split("_")[1]

            aliases_with_attributes = self.connect_aliases_with_attributes(
                cte_name, prop, after_union_parsed["select"], before_union_parsed)

            path_expression += "MATCH (m : " + prop + \
                ") -[" + edge_label + "*0..] -> (n :" + prop + ")\n"

            path_expression += "WHERE " + unwind_var + "." + pk2 + "= m." + pk + "\n"

            path_expression += "WITH collect({ "
            for i, alias_attribute in enumerate(aliases_with_attributes):
                prop = self.cte[cte_name]["attributes"][i]
                if i == len(aliases_with_attributes) - 1:
                    path_expression += prop + " : " + alias_attribute + "}) AS " + cte_name + "\n"
                else:
                    path_expression += prop + " : " + alias_attribute + ", "
        else:
            print("Not supported when there are more tables than one!")

        query += initial_node + path_expression
        return query

    def assign_keyword_parts(self, cte_name, orig_query):
        query = dict()
        current = ""
        for elem in orig_query:
            if current != "":
                if elem not in KEYWORDS:
                    cleaned = elem.replace(",", "").strip()
                    if cleaned != "" and cleaned != cte_name:
                        query[current].append(cleaned)
            if elem in KEYWORDS:
                current = elem
                query[current] = []
        return query

    def parse_edge_label(self, cte_name, before_union_parsed, after_union_parsed):
        connection = after_union_parsed["where"]
        if len(connection) == 1:
            conn = connection[0]
            parts = conn.split("=")
            primary, foreign = None, None
            for part in parts:
                part = part.strip()
                if "." in part:
                    part = part.split(".")[1]
                if self.db.is_primary_key(part):
                    primary = part
                elif self.db.is_foreign_key(part):
                    foreign = part
                else:
                    if foreign == None:
                        i = self.cte[cte_name]["attributes"].index(part)
                        foreign = before_union_parsed["select"][i]
                    elif primary == None:
                        i = self.cte[cte_name]["attributes"].index(part)
                        primary = before_union_parsed["select"][i]
            return primary, foreign + "_" + primary
        return None

    def connect_aliases_with_attributes(self, cte_name, table, attributes, before_union_parsed):
        result = []
        table_attributes = self.db.get_attributes_for_table(table)
        for attr in attributes:
            if attr in table_attributes:
                result.append("n." + attr)
            elif attr in self.cte[cte_name]["attributes"]:
                i = self.cte[cte_name]["attributes"].index(attr)
                corresponding_attr = before_union_parsed["select"][i]
                result.append("m." + corresponding_attr)
            else:
                print("Attribute not found: ", attr)
        return result


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
