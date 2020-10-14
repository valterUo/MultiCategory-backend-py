import re
import itertools
import random
import string
from model_transformations.query_language_transformations.SQL.components.select import SELECT
from model_transformations.query_language_transformations.SQL.components.from_part import FROM
from model_transformations.query_language_transformations.SQL.components.where import WHERE
from model_transformations.query_language_transformations.SQL.components.group_by import GROUPBY
from model_transformations.query_language_transformations.SQL.components.order_by import ORDERBY
from model_transformations.query_language_transformations.SQL.components.join import JOIN
from model_transformations.query_language_transformations.Cypher.cypher import Cypher

KEYWORDS = ['select', 'from', 'where', 'inner join', 'outer join',
            'left join', 'right join', 'full join', 'group by', 'order by', 'limit']

## Aggregating functions are not allowed inside aggregating functions in Cypher. On the other hand, SQL allows to nest them. For Cypher we need to unnest them.
cypher_aggregating_functions = ["collect", "sum", "count", "max", "min", "avg", "percentileCont", "percentileDisc", "stDev", "stDevP"]


class SQL:

    def __init__(self, name, query_string, rel_db, primary_foreign_keys = [], full_query_common_table_expression_names = [], previous_ctes = []):
        self.name = name
        self.original_query = query_string
        self.rel_db = rel_db
        self.pk_fk_contrainsts = self.rel_db.get_all_pk_fk_contrainsts()
        self.primary_foreign_keys = primary_foreign_keys
        self.previous_ctes = previous_ctes
        self.columns_datatypes = rel_db.get_all_columns_datatypes()
        self.query_string = self.remove_comments(query_string.strip().lower())
        self.query = dict()
        self.common_table_expressions = self.parse_common_table_expressions()
        self.full_query_common_table_expression_names = full_query_common_table_expression_names

        for table in  self.pk_fk_contrainsts:
            self.primary_foreign_keys += list(self.pk_fk_contrainsts[table].keys())
            for constraint in  self.pk_fk_contrainsts[table].values():
                self.primary_foreign_keys.append(constraint["primary_key_in_target_table"])

        if full_query_common_table_expression_names == []:
            self.full_query_common_table_expression_names = list(self.common_table_expressions.keys())
        if self.common_table_expressions["main"] != "":
            for elem in self.common_table_expressions:
                previous_ctes = list(itertools.takewhile(lambda ele: ele != elem, self.common_table_expressions))
                self.query[elem] = SQL(elem, self.common_table_expressions[elem], self.rel_db, self.primary_foreign_keys, self.full_query_common_table_expression_names, previous_ctes)
        else:
            #print(self.query_string)
            if self.query_string.count("select") == 1:
                keyword_sequence = self.get_keyword_sequence()
                for i in range(len(keyword_sequence)):
                    if i < len(keyword_sequence) - 1:
                        keyword_from = keyword_sequence[i]
                        keyword_to = keyword_sequence[i+1]
                        ex = re.compile(
                            r'(?<=' + keyword_from + r')' + r'.*?' + r'(?=' + keyword_to + r')', re.DOTALL)
                        result = re.search(ex, self.query_string)
                        #print(keyword_from, result)
                        if result != None:
                            self.query[keyword_from] = result.group()
                    else:
                        keyword_from = keyword_sequence[i]
                        ex = re.compile(
                            r'(?<=' + keyword_from + r')' + r'.+', re.DOTALL)
                        result = re.search(ex, self.query_string)
                        #print(keyword_from, result)
                        if result != None:
                            self.query[keyword_from] = result.group()
            # for elem in self.query:
            #     print(elem, self.query[elem])
            for elem in self.query:
                if elem == "select":
                    select_result = SELECT(self.query[elem])
                    self.query[elem] = select_result
                    self.primary_foreign_keys += select_result.get_keys()
                    #print(self.query[elem].get_attributes())
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
                elif elem == "full join":
                    self.query[elem] = JOIN(
                        "full", self.query[elem], self.query["from"])
                elif elem == "inner join":
                    self.query[elem] = JOIN(
                        "inner", self.query[elem], self.query["from"])

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
        return ctes

    def get_keyword_sequence(self):
        keyword_sequence = list()
        words = re.split(r'\s', self.query_string)
        for i in range(len(words) - 1):
            if words[i].strip() in KEYWORDS:
                keyword_sequence.append(words[i].strip())
            elif words[i].strip() + " " + words[i+1].strip() in KEYWORDS:
                keyword_sequence.append(
                    words[i].strip() + " " + words[i+1].strip())
        return keyword_sequence

    @staticmethod
    def get_cypher(self, cte=True, cte_name=""):
        query = ""
        if self.common_table_expressions["main"] != "":
            for elem in self.common_table_expressions:
                if elem != "main":
                    query += self.get_cypher(self.query[elem], True, elem)
                else:
                    query += self.get_cypher(self.query[elem], False)
        else:
            if 'where' in self.query.keys():
                query += self.transform_select_from_join_into_graph_patterns(
                    self.query["select"], self.query["from"], self.query["where"], cte, cte_name)
            if 'full join' in self.query.keys():
                query += self.transform_select_from_join_into_graph_patterns(
                    self.query["select"], self.query["from"], self.query["full join"], cte, cte_name)
        return query

    def transform_select_from_join_into_graph_patterns(self, select_part, from_part, join_part, cte=False, cte_name=""):
        query = ""
        join_type = join_part.get_join_type()
        connections = join_part.get_join_conditions()
        where_clause = False
        table_aliases_in_query = []
        if len(connections) == 0:
            for table in from_part.get_tables():
                if table[1] != None:
                    query += "MATCH (" + table[1] + ":" + table[0] + ")\n"
                else:
                    query += "MATCH (" + table[0] + ")\n"
        else:
            any_of_tables_refering_ctes = False
            for table in from_part.get_tables():
                if table[0] in self.full_query_common_table_expression_names:
                    any_of_tables_refering_ctes = True
            if any_of_tables_refering_ctes:
                table_aliases = []
                for table in from_part.get_tables():
                    if table[0] in self.full_query_common_table_expression_names:
                        query += "UNWIND " + table[0] + " AS " + table[1] + "\n"
                        table_aliases.append(table[1])
                    else:
                        query += "MATCH (" + table[1] + " : " + table[0] + ")\n"
                if table_aliases != []:
                    previous_cte = ""
                    for prev_cte in self.previous_ctes:
                        previous_cte += prev_cte + ", "
                    query += "WITH " + previous_cte
                    for i in range(len(table_aliases)):
                        elem = table_aliases[i]
                        if i == len(table_aliases) - 1:
                            query += elem + " AS " + elem + "\n"
                        else:
                            query += elem + " AS " + elem + ", "
            for k in range(len(connections)):
                connection = connections[k]
                alias1, alias2 = connection[0][0].strip(), connection[2][0].strip()
                key1, key2 = connection[0][1].strip(), connection[2][1].strip()
                property1, property2 = from_part.get_table_from_alias(alias1), from_part.get_table_from_alias(alias2)
                table_aliases_in_query += [alias1, alias2]
                ## Arrows are pointing from foreign to primary, we need to see which one is which one
                if property1 in self.full_query_common_table_expression_names or property2 in self.full_query_common_table_expression_names:
                    for t in range(k, len(connections)):
                        connection = connections[t]
                        alias1, alias2 = connection[0][0].strip(), connection[2][0].strip()
                        key1, key2 = connection[0][1].strip(), connection[2][1].strip()
                        property1, property2 = from_part.get_table_from_alias(alias1), from_part.get_table_from_alias(alias2)
                        if k > t:
                            table_aliases_in_query += [alias1, alias2]
                        if property1 or property2 in self.full_query_common_table_expression_names:
                            if not where_clause:
                                query += "WHERE " + alias1 + "." + key1 + " = " + alias2 + "." + key2 + "\n"
                                where_clause = True
                            else:
                                query += "AND " + alias1 + "." + key1 + " = " + alias2 + "." + key2 + "\n"
                        else:
                            k = t
                            break
                else:
                    source_property, source_alias, foreign_key, target_property, target_alias, primary_key = None, None, None, None, None, None
                    if key1 in self.pk_fk_contrainsts[property1].keys() or key1 in self.pk_fk_contrainsts[property2].keys():
                        source_property = property1
                        source_alias = alias1
                        foreign_key = key1
                        target_property = property2
                        target_alias = alias2
                        primary_key = key2
                    elif key2 in self.pk_fk_contrainsts[property1].keys() or key2 in self.pk_fk_contrainsts[property2].keys():
                        source_property = property2
                        source_alias = alias2
                        foreign_key = key2
                        target_property = property1
                        target_alias = alias1
                        primary_key = key1
                    prefix = ""
                    connection_name = foreign_key + "_" + primary_key
                    if join_type == "full" or join_type == "outer":
                        prefix = "OPTIONAL "
                    if source_property != None and target_property != None:
                        query += prefix + "MATCH (" + source_alias + " : " + source_property + ") -[" + connection_name + "]-> (" + target_alias + " : " + target_property + ")\n"
                    elif source_property != None:
                        query += prefix + "MATCH (" + source_alias + " : " + source_property + ") -[" + connection_name + "]-> (" + target_property + ")\n"
                    elif target_property != None:
                        query += prefix + "MATCH (" + source_alias + ") -[" + connection_name + "]-> (" + target_alias + " : " + target_property + ")\n"
                    else:
                        query += prefix + "MATCH (" + source_alias + ") -[" + connection_name + "]-> (" + target_alias + ")\n"
        if len(join_part.get_filtering_conditions()) > 0:
            filtering_clause = "WHERE "
            if where_clause:
                filtering_clause = "AND "
            i = 0
            for filtering_condition in join_part.get_filtering_conditions():
                for elem in filtering_condition:
                    if type(elem) == tuple or type(elem) == list:
                        attr = elem[1].strip()
                        if attr in self.columns_datatypes.keys():
                            if 'timestamp' in self.columns_datatypes[attr]:
                                filtering_clause += "datetime(" + elem[0] + "." + attr + ")"
                            else:
                                filtering_clause += elem[0] + "." + elem[1]
                        else:
                                filtering_clause += elem[0] + "." + elem[1]
                    else:
                        filtering_clause += elem
                if i == len(join_part.get_filtering_conditions()) - 1:
                    filtering_clause += "\n"
                else:
                    filtering_clause += " AND \n"
                i+=1
            query += filtering_clause
        return_clause = "RETURN "
        if cte:
            return_clause = ""
            i = 0
            comma = ","
            for attribute in select_part.get_attributes():
                #print(attribute)
                if i == len(select_part.get_attributes()) - 1:
                    comma = ""
                if attribute[0] != None and attribute[1] != None and attribute[2] != None:
                    return_clause += attribute[2] + " : " + attribute[0] + "." + attribute[1] + comma + " "
                    self.primary_foreign_keys.append(attribute[2])
                elif attribute[0] == None and attribute[2] != None:
                    return_clause += attribute[2] + " : " + attribute[1] + comma + " "
                    self.primary_foreign_keys.append(attribute[2])
                elif attribute[0] == None and attribute[2] == None:
                    return_clause += attribute[1] + comma + " "
                elif attribute[0] != None and attribute[2] == None:
                    return_clause += attribute[0] + "." + attribute[1] + comma + " "
                i += 1
            aggre_funs = ""
            for aggre_fun in cypher_aggregating_functions:
                if aggre_fun in return_clause:
                    variable = get_random_string(3)
                    cut_fun = re.search(aggre_fun + r'(.+)', return_clause).groups()
                    cut_fun = aggre_fun + cut_fun[0]
                    return_clause = return_clause.replace(cut_fun, variable)
                    aggre_funs += cut_fun + " AS " + variable + ", "
            previous_cte = ""
            for prev_cte in self.previous_ctes:
                previous_cte += prev_cte + ", "
            table_alias_part = ""
            for table_alias in table_aliases_in_query:
                #print(table_alias)
                if " " + table_alias + "." in return_clause:
                    table_alias_part += table_alias + ", "
                    print(table_alias_part)
            sub_result = aggre_funs + previous_cte + table_alias_part
            if sub_result != "":
                sub_result = sub_result[:-2]
                query += "WITH " + sub_result + "\n"
            return_clause = "WITH "+ previous_cte + "collect({ " + return_clause
            if cte_name != None and cte_name != "":
                #print("cte_name: ", cte_name)
                return_clause += "}) AS " + cte_name + "\n"
            else:
                return_clause += "})\n"
        else:
            i = 0
            comma = ","
            for attribute in select_part.get_attributes():
                if i == len(select_part.get_attributes()) - 1:
                    comma = ""
                if attribute[0] != None and attribute[2] != None:
                    return_clause += attribute[0] + "." + \
                        attribute[1] + " AS " + attribute[2] + comma + " "
                elif attribute[0] == None and attribute[2] == None:
                    return_clause += attribute[1] + comma + " "
                elif attribute[2] == None:
                    return_clause += attribute[0] + \
                        "." + attribute[1] + comma + " "
                elif attribute[0] == None:
                    return_clause += attribute[1] + \
                        " AS " + attribute[2] + comma + " "
                i += 1
        query += return_clause + "\n"
        if 'order by' in self.query.keys():
            query += self.query['order by'].get_order_by_cypher() + "\n"
        return query

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
