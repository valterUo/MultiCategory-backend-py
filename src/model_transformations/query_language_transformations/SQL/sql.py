import re
import itertools
import random
from re import search
import string
from model_transformations.query_language_transformations.SQL.components.select import SELECT
from model_transformations.query_language_transformations.SQL.components.from_part import FROM
from model_transformations.query_language_transformations.SQL.components.where import WHERE
from model_transformations.query_language_transformations.SQL.components.group_by import GROUPBY
from model_transformations.query_language_transformations.SQL.components.order_by import ORDERBY
from model_transformations.query_language_transformations.SQL.components.join import JOIN

KEYWORDS = ['select', 'from', 'where', 'inner join', 'outer join', 'left join', 'right join', 'full join', 'group by', 'order by', 'limit']

## Aggregating functions are not allowed inside aggregating functions in Cypher. On the other hand, SQL allows to nest them. For Cypher we need to unnest them.
cypher_aggregating_functions = ["collect", "sum", "count", "max", "min", "avg", "percentileCont", "percentileDisc", "stDev", "stDevP"]


class SQL:

    def __init__(self, name, query_string, rel_db, primary_foreign_keys = [], all_cte_names = [], previous_ctes = []):
        self.name = name
        self.original_query = query_string
        self.rel_db = rel_db
        self.pk_fk_contrainsts = self.rel_db.get_all_pk_fk_contrainsts()
        self.primary_foreign_keys = primary_foreign_keys
        self.previous_ctes = previous_ctes
        self.columns_datatypes = rel_db.get_all_columns_datatypes()
        self.query_string = remove_comments(query_string.strip().lower())
        self.query = dict()
        self.common_table_expressions = self.parse_common_table_expressions()
        self.all_cte_names = all_cte_names
        self.where_keyword_used = False

        for table in  self.pk_fk_contrainsts:
            self.primary_foreign_keys += list(self.pk_fk_contrainsts[table].keys())
            for constraint in  self.pk_fk_contrainsts[table].values():
                self.primary_foreign_keys.append(constraint["primary_key_in_target_table"])

        if all_cte_names == []:
            self.all_cte_names = list(self.common_table_expressions.keys())
        if self.common_table_expressions["main"] != "":
            for elem in self.common_table_expressions:
                previous_ctes = list(itertools.takewhile(lambda ele: ele != elem, self.common_table_expressions))
                self.query[elem] = SQL(elem, self.common_table_expressions[elem], self.rel_db, self.primary_foreign_keys, self.all_cte_names, previous_ctes)
        else:
            keyword_sequence = self.get_keyword_sequence()
            for i in range(len(keyword_sequence)):
                if i < len(keyword_sequence) - 1:
                    keyword_from = keyword_sequence[i]
                    keyword_to = keyword_sequence[i+1]
                    result = parse_query_with_keywords(keyword_from, self.query_string, keyword_to)
                    self.query[keyword_from] = result
                else:
                    keyword_from = keyword_sequence[i]
                    result = parse_query_with_keywords(keyword_from, self.query_string)
                    self.query[keyword_from] = result
            keyword_sequence.remove("from")
            keyword_sequence.insert(0, "from")
            for elem in keyword_sequence:
                if elem == "from":
                    self.query[elem] = FROM(self.query[elem])
                elif elem == "select":
                    select_result = SELECT(self.query[elem], self.query['from'], self.rel_db)
                    self.query[elem] = select_result
                    self.primary_foreign_keys += select_result.get_keys()
                elif elem == "where":
                    self.query[elem] = WHERE(self.query[elem], self.primary_foreign_keys, self.query['from'], self.rel_db)
                elif elem == "group by":
                    self.query[elem] = GROUPBY(self.query[elem])
                elif elem == "order by":
                    self.query[elem] = ORDERBY(self.query[elem])
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
        keyword_sequence = list(dict.fromkeys(keyword_sequence))
        return keyword_sequence

    @staticmethod
    def get_cypher(self, cte_name=""):
        query = ""
        cte = True
        if cte_name == 'main':
            cte = False
        if self.common_table_expressions["main"] != "":
            for elem in self.common_table_expressions:
                if elem != "main":
                    query += self.get_cypher(self.query[elem], elem)
                else:
                    query += self.get_cypher(self.query[elem], 'main')
        else:
            if 'where' in self.query.keys():
                query += self.transform_into_cypher(self.query["select"], self.query["from"], cte, cte_name, self.query["where"])
            elif 'full join' in self.query.keys():
                query += self.transform_into_cypher(self.query["select"], self.query["from"], cte, cte_name, self.query["full join"])
            else:
                query += self.transform_into_cypher(self.query["select"], self.query["from"], cte, cte_name)
        return query

    def transform_into_cypher(self, select_part, from_part, cte, cte_name, join_part = None):
        query = ""
        connections = []
        conds = []
        if join_part != None:
            join_type = join_part.get_join_type()
            connections = join_part.get_join_conditions()
            conds = join_part.get_filtering_conditions()
        table_aliases_in_query = []
        tables = from_part.get_tables()
        if len(connections) == 0:
            query += parse_query_without_connections(from_part)
            #query += self.parse_collected_cte_for_use(tables, from_part)
        else:
            query += self.parse_collected_cte_for_use(tables, from_part)
            query += self.parse_joins(connections, table_aliases_in_query, from_part, join_type)
        if len(conds) > 0:
            query += self.parse_filtering_conditions(conds)
        if cte:
            query += self.parse_cte_with_collect(select_part.get_attributes(), table_aliases_in_query, cte_name)
        else:
            query += parse_return_clause(select_part)
        if 'order by' in self.query.keys():
            query += self.query['order by'].get_order_by_cypher() + "\n"
        return query

    def parse_match_patterns_based_on_joins(self, property1, property2, key1, key2, alias1, alias2, join_type):
        query, prefix = "", ""
        source_property, source_alias, foreign_key, target_property, target_alias, primary_key = None, None, None, None, None, None
        property1_keys = self.pk_fk_contrainsts[property1].keys()
        property2_keys = self.pk_fk_contrainsts[property2].keys()
        if key1 in property1_keys or key1 in property2_keys:
            source_property, target_property = property1, property2
            source_alias, target_alias = alias1, alias2
            foreign_key, primary_key = key1, key2
        elif key2 in property1_keys or key2 in property2_keys:
            source_property, target_property = property2, property1
            source_alias, target_alias = alias2, alias1
            foreign_key, primary_key = key2, key1
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
        return query

    def parse_filtering_conditions(self, conds):
        result = "WHERE "
        if self.where_keyword_used:
            result = "AND "
        else:
            self.where_keyword_used = True
        i = 0
        for filtering_condition in conds:
            for elem in filtering_condition:
                if type(elem) == tuple or type(elem) == list:
                    attr = elem[1].strip()
                    if elem[0] != None:
                        if attr in self.columns_datatypes.keys():
                            if 'timestamp' in self.columns_datatypes[attr]:
                                result += "datetime(" + elem[0] + "." + attr + ")"
                            else:
                                result += elem[0] + "." + elem[1]
                        else:
                                result += elem[0] + "." + elem[1]
                    else:
                        result += attr
                else:
                    result += elem
            if i == len(conds) - 1:
                result += "\n"
            else:
                result += " AND \n"
            i+=1
        return result

    def parse_cte_with_collect(self, attributes, table_aliases_in_query, cte_name):
        result = ""
        for attribute in attributes:
            if attribute[0] != None and attribute[1] != None and attribute[2] != None:
                result += attribute[2] + " : " + attribute[0] + "." + attribute[1] + ", "
                self.primary_foreign_keys.append(attribute[2])
            elif attribute[0] == None and attribute[2] != None:
                result += attribute[2] + " : " + attribute[1] + ", "
                self.primary_foreign_keys.append(attribute[2])
            elif attribute[0] == None and attribute[2] == None:
                result += attribute[1] + ", "
            elif attribute[0] != None and attribute[2] == None:
                result += attribute[0] + "." + attribute[1] + ", "
        result = result[:-2]
        aggre_funs = ""
        for aggre_fun in cypher_aggregating_functions:
            if aggre_fun in result:
                variable = get_random_string(3)
                cut_fun = re.search(aggre_fun + r'(.+)', result).groups()
                cut_fun = aggre_fun + cut_fun[0]
                result = result.replace(cut_fun, variable)
                aggre_funs += cut_fun + " AS " + variable + ", "
        previous_cte = ""
        for prev_cte in self.previous_ctes:
            previous_cte += prev_cte + ", "
        table_alias_part = ""
        for table_alias in table_aliases_in_query:
            if " " + table_alias + "." in result:
                table_alias_part += table_alias + ", "
        sub_result = aggre_funs + previous_cte + table_alias_part
        if sub_result != "":
            sub_result = "WITH " + sub_result[:-2]+ "\n"
        result = sub_result + "WITH "+ previous_cte + "collect({ " + result
        if cte_name != None and cte_name != "":
            result += "}) AS " + cte_name + "\n"
        else:
            result += "})\n"
        return result + "\n"

    def parse_collected_cte_for_use(self, tables, from_part):
        result = ""
        any_of_tables_refering_ctes = False
        for table in tables:
            if table[0] in self.all_cte_names:
                any_of_tables_refering_ctes = True
        if any_of_tables_refering_ctes:
            table_aliases = []
            for table in tables:
                if table[0] in self.all_cte_names:
                    result += "UNWIND " + table[0] + " AS " + table[1] + "\n"
                    table_aliases.append(table[1])
                else:
                    result += "MATCH (" + table[1] + " : " + table[0] + ")\n"
            if table_aliases != []:
                previous_cte = ""
                for prev_cte in self.previous_ctes:
                    previous_cte += prev_cte + ", "
                result += "WITH " + previous_cte
                for i in range(len(table_aliases)):
                    elem = table_aliases[i]
                    if i == len(table_aliases) - 1:
                        result += elem + "\n"
                    else:
                        result += elem + ", "
        #else:
        #    result += parse_query_without_connections(from_part)
        return result

    def parse_joins(self, connections, table_aliases_in_query, from_part, join_type):
        result = ""
        checked = []
        for k, connection in enumerate(connections):
            property1, alias1, key1, property2, alias2, key2 = get_property_alias_key_from_connection(from_part, connection)
            table_aliases_in_query += [alias1, alias2]
            ## Arrows are pointing from foreign to primary, we need to see which one is which one
            if property1 in self.all_cte_names or property2 in self.all_cte_names:
                for t in range(k, len(connections)):
                    if t not in checked:
                        checked.append(t)
                        connection = connections[t]
                        property1, alias1, key1, property2, alias2, key2 = get_property_alias_key_from_connection(from_part, connection)
                        if t > k:
                            table_aliases_in_query += [alias1, alias2]
                        if property1 or property2 in self.all_cte_names:
                            if not self.where_keyword_used:
                                result += "WHERE " + alias1 + "." + key1 + " = " + alias2 + "." + key2 + "\n"
                                self.where_keyword_used = True
                            else:
                                result += "AND " + alias1 + "." + key1 + " = " + alias2 + "." + key2 + "\n"
                        else:
                            break
            else:
                result += self.parse_match_patterns_based_on_joins(property1, property2, key1, key2, alias1, alias2, join_type)
                checked.append(k)
        return result

def remove_comments(query):
    ## Multi-line comments
    multi_line_comment_ex = re.compile(r'(\/\*).*(\*\/)', re.DOTALL)
    result = re.sub(multi_line_comment_ex, '', query)
    ## One line comments
    result = re.sub(r'(--).*(\n|\r|\rn)', '', result)
    return result.strip()

def parse_query_with_keywords(keyword_from, query, keyword_to = None):
    start_indexes = [m.start() for m in re.finditer(keyword_from, query)]
    result = ""
    if len(start_indexes) > 0:
        for start_index in start_indexes:
            result = ""
            paranthesis = []
            ending_indexes = [-1]
            search_part = query[start_index:]
            if keyword_to != None:
                ending_indexes = [m.start() for m in re.finditer(keyword_to, search_part)]
            for i, c in enumerate(search_part):
                if c == "(":
                    paranthesis.append("(")
                elif c == ")":
                    if len(paranthesis) > 0:
                        paranthesis.pop()
                    else:
                        break
                for j in ending_indexes:
                    if i == j and len(paranthesis) == 0:
                        result = result.replace(keyword_from, "", 1)
                        #result = result.replace(keyword_to, "", 1)
                        result = result.strip()
                        return result
                result += c
        result = result.replace(keyword_from, "", 1)
        return result

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def parse_query_without_connections(from_part):
    query = ""
    for table in from_part.get_tables():
        if table[1] != None:
            query += "MATCH (" + table[1] + ":" + table[0] + ")\n"
        else:
            query += "MATCH (" + table[0] + ")\n"
    return query

def parse_return_clause(select_part):
    result = ""
    for attr in select_part.get_attributes():
        if attr[0] != None and attr[2] != None:
            result += attr[0] + "." + attr[1] + " AS " + attr[2] + ", "
        elif attr[0] == None and attr[2] == None:
            result += attr[1] + ", "
        elif attr[2] == None:
            result += attr[0] + "." + attr[1] + ", "
        elif attr[0] == None:
            result += attr[1] + " AS " + attr[2] + ", "
    return "RETURN " + result[:-2] + "\n"

def get_property_alias_key_from_connection(from_part, connection):
    alias1, alias2 = connection[0][0].strip(), connection[2][0].strip()
    key1, key2 = connection[0][1].strip(), connection[2][1].strip()
    property1, property2 = from_part.get_table_from_alias(alias1), from_part.get_table_from_alias(alias2)
    return property1, alias1, key1, property2, alias2, key2