import re
from re import error
from model_transformations.query_language_transformations.SQL.components.select import SELECT
from model_transformations.query_language_transformations.SQL.components.from_part import FROM
from model_transformations.query_language_transformations.SQL.components.where import WHERE
from model_transformations.query_language_transformations.SQL.components.group_by import GROUPBY
from model_transformations.query_language_transformations.SQL.components.order_by import ORDERBY
from model_transformations.query_language_transformations.SQL.components.join import JOIN
from model_transformations.query_language_transformations.Cypher.cypher import Cypher

KEYWORDS = ['select', 'from', 'where', 'inner join', 'outer join', 'left join', 'right join', 'full join', 'group by', 'order by', 'limit']

class SQL:

    def __init__(self, name, query_string, primary_foreign_keys):
        self.name = name
        self.original_query = query_string
        self.primary_foreign_keys = primary_foreign_keys
        self.query_string = self.remove_comments(query_string.strip().lower())
        self.query = dict()
        self.common_table_expressions = self.parse_common_table_expressions()
        if self.common_table_expressions["main"] != "":
            for elem in self.common_table_expressions:
                self.query[elem] = SQL(elem, self.common_table_expressions[elem])
        else:
            #print(self.query_string)
            if self.query_string.count("select") == 1:
                keyword_sequence = self.get_keyword_sequence()
                for i in range(len(keyword_sequence)):
                    if i < len(keyword_sequence) - 1:
                        keyword_from = keyword_sequence[i]
                        keyword_to = keyword_sequence[i+1]
                        ex = re.compile(r'(?<=' + keyword_from + r')' + r'.*?' + r'(?=' + keyword_to + r')', re.DOTALL)
                        result = re.search(ex, self.query_string)
                        #print(keyword_from, result)
                        if result != None:
                            self.query[keyword_from] = result.group()
                    else:
                        keyword_from = keyword_sequence[i]
                        ex = re.compile(r'(?<=' + keyword_from + r')' + r'.+', re.DOTALL)
                        result = re.search(ex, self.query_string)
                        #print(keyword_from, result)
                        if result != None:
                            self.query[keyword_from] = result.group()
            # for elem in self.query:
            #     print(elem, self.query[elem])
            for elem in self.query:
                if elem == "select":
                    self.query[elem] = SELECT(self.query[elem])
                    print(self.query[elem].get_attributes())
                elif elem == "from":
                    self.query[elem] = FROM(self.query[elem])
                    #print(self.query[elem].get_tables())
                elif elem == "where":
                    self.query[elem] = WHERE(self.query[elem], self.primary_foreign_keys)
                    #print(self.query[elem].get_conjunctive_part())
                    #print(self.query[elem].get_disjunctive_part())
                elif elem == "group by":
                    self.query[elem] = GROUPBY(self.query[elem])
                    #print(self.query[elem].get_attributes())
                elif elem == "order by":
                    self.query[elem] = ORDERBY(self.query[elem])
                    #print(self.query[elem].get_attributes())

    def get_name(self):
        return self.name

    def get_sql_query(self):
        return self.original_query

    def remove_comments(self, query):
        ## Multi-line comments
        multi_line_comment_ex = re.compile(r'(\/\*).*(\*\/)', re.DOTALL)
        result = re.sub(multi_line_comment_ex, '', query)
        ## One line comments
        result = re.sub(r'(--).*(\n|\r|\rn)', '', result)
        return result.strip()
        
    def parse_common_table_expressions(self):
        ctes = dict()
        collecting, collecting_name, collecting_subquery, collecting_main = False, False, False, False
        name, subquery, main_query, paranthesis = "", "", "", []
        for i in range(len(self.query_string)):
            if self.query_string[i-4:i] == "with":
                collecting = True
                collecting_name = True
            if collecting_name:
                if self.query_string[i:i+2] == "as":
                    collecting_name = False
                    collecting_subquery = True
                else:
                    name += self.query_string[i]
            if collecting_subquery:
                subquery += self.query_string[i]
                if self.query_string[i] == "(":
                    paranthesis.append("(")
                if self.query_string[i] == ")":
                    paranthesis.pop()
                    if len(paranthesis) == 0:
                        ctes[name.strip()] = subquery
                        name, subquery = "", ""
                        collecting_subquery = False
            if collecting and not collecting_subquery and not collecting_name and not collecting_main:
                if self.query_string[i] == ",":
                    collecting_name = True
                else:
                    if re.match(r'[a-z]', self.query_string[i]) != None:
                        collecting_main = True
            if collecting_main and collecting:
                main_query += self.query_string[i]

        ctes["main"] = main_query
        ex = re.compile(r'(?<=\().+(?=\))', re.DOTALL)
        ex2 = re.compile(r'\s\s+')
        for elem in ctes:
            if elem != "main":
                try:
                    ctes[elem] = re.search(ex, ctes[elem]).group()
                except:
                    pass
            ctes[elem] = re.sub(ex2, ' ', ctes[elem])
        # for elem in ctes:
        #     print(elem)
        #     print()
        #     print(ctes[elem])
        #     print("-----------------------------------------------")
        return ctes


    def get_keyword_sequence(self):
        keyword_sequence = list()
        words = re.split(r'\s', self.query_string)
        for i in range(len(words) - 1):
            if words[i].strip() in KEYWORDS:
                keyword_sequence.append(words[i].strip())
            elif words[i].strip() + " " + words[i+1].strip() in KEYWORDS:
                keyword_sequence.append(words[i].strip() + " " + words[i+1].strip())
        return keyword_sequence

    ## This function works so that 
    def get_cypher(self):
        query = ""
        if self.common_table_expressions["main"] != "":
            for elem in self.common_table_expressions:
                if elem != "main":
                    query = query + self.query[elem].get_cypher()
        else:
            try:
                query += self.transform_select_from_join_into_graph_patterns(self.query["select"], self.query["from"], self.query["where"])
            except:
                raise error
        return query

    def transform_select_from_join_into_graph_patterns(self, select_part, from_part, where_part):
        query = ""
        connections = where_part.get_join_conditions()
        print(connections)
        for table in from_part.get_tables():
            if table[1] != None:
                query += "MATCH (" + table[1] + ":" + table[0] + ")\n"
            else:
                query += "MATCH (" + table[0] + ")\n"
        return_clause = "RETURN "
        for attribute in select_part.get_attributes():
            if attribute[0] != None and attribute[2] != None:
                return_clause += attribute[0] + "." + attribute[1] + " AS " + attribute[2] + " "
            elif attribute[0] == None and attribute[2] == None:
                return_clause += attribute[1] + " "
            elif attribute[2] == None:
                return_clause += attribute[0] + "." + attribute[1] + " "
            elif attribute[0] == None:
                return_clause += attribute[1] + " AS " + attribute[2] + " "
        query += return_clause
        print(query)
        return query