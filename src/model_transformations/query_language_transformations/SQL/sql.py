import re
import itertools
from collections import OrderedDict
from model_transformations.query_language_transformations.SQL.components.select import SELECT
from model_transformations.query_language_transformations.SQL.components.from_part import FROM
from model_transformations.query_language_transformations.SQL.components.where import WHERE
from model_transformations.query_language_transformations.SQL.components.group_by import GROUPBY
from model_transformations.query_language_transformations.SQL.components.order_by import ORDERBY
from model_transformations.query_language_transformations.SQL.components.join import JOIN
from model_transformations.query_language_transformations.SQL.global_variables import CYPHER_AGGREGATING_FUNCTIONS
from model_transformations.query_language_transformations.SQL.independent_sql_parsing_tools import *

## Instance of SQL class contain 0 or multiple common table expressions, 0 or multiple subqueries and exactly one so called main query

class SQL:

    def __init__(self, name, query_string, rel_db, primary_foreign_keys = [], all_cte_names = [], previous_ctes = [], main_block = True):
        self.name = name
        self.original_query = query_string
        self.rel_db = rel_db
        self.main_block = main_block
        self.pk_fk_contrainsts = self.rel_db.get_all_pk_fk_contrainsts()
        self.primary_foreign_keys = primary_foreign_keys
        self.previous_ctes = previous_ctes
        self.columns_datatypes = rel_db.get_all_columns_datatypes()
        self.query_string = remove_comments(query_string.replace(";", "").strip().lower())
        self.query = OrderedDict()
        self.ctes = OrderedDict()
        self.subqueries = []
        self.unparsed_ctes = extract_common_table_expressions(self.query_string)
        self.all_cte_names = all_cte_names
        self.where_keyword_used = False
        self.from_part = None

        for table in  self.pk_fk_contrainsts:
            self.primary_foreign_keys += list(self.pk_fk_contrainsts[table].keys())
            for constraint in  self.pk_fk_contrainsts[table].values():
                self.primary_foreign_keys.append(constraint["primary_key_in_target_table"])

        if all_cte_names == []:
            self.all_cte_names = list(self.unparsed_ctes.keys())
            self.all_cte_names.remove("main")
        
        for elem in self.unparsed_ctes:
            previous_ctes = list(itertools.takewhile(lambda ele: ele != elem, self.unparsed_ctes))
            if elem != "main":
                self.ctes[elem] = SQL(elem, self.unparsed_ctes[elem], self.rel_db, self.primary_foreign_keys, self.all_cte_names, previous_ctes, False)
            else:
                self.parse_main_query()

        self.cypher_query = self.transform()
            
    def get_name(self):
        return self.name

    def get_sql_query(self):
        return self.original_query

    def get_cypher(self):
        return self.cypher_query

    def parse_main_query(self):
        keyword_sequence = get_keyword_sequence(self.unparsed_ctes["main"])
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
                self.from_part = FROM(self.query[elem])
                self.query[elem] = self.from_part
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

    def transform(self):
        query = ""
        for elem in self.ctes:
            query += self.ctes[elem].get_cypher()
        if 'where' in self.query.keys():
            query += self.transform_into_cypher(self.query["select"], self.query["where"])
        elif 'full join' in self.query.keys():
            query += self.transform_into_cypher(self.query["select"], self.query["full join"])
        else:
            query += self.transform_into_cypher(self.query["select"])
        return query

    def transform_into_cypher(self, select_part, join_part = None):
        query, join_type = "", ""
        connections, conds = [], []

        if join_part != None:
            join_type = join_part.get_join_type()
            connections = join_part.get_join_conditions()
            conds = join_part.get_filtering_conditions()
        table_aliases_in_query = []
        tables = self.from_part.get_tables()
        for table in tables:
            table_aliases_in_query.append(table[0])
        if len(connections) == 0:
            query += self.parse_query_without_connections(tables)
        else:
            query += self.parse_collected_cte_for_use(tables)
            query += self.parse_joins(connections, table_aliases_in_query, join_type)
        if len(conds) > 0:
            query += self.parse_filtering_conditions(conds)
        if self.main_block:
            query += self.parse_return_clause(select_part)
        else:
            query += self.parse_cte_with_collect(select_part.get_attributes(), table_aliases_in_query)
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
        for i, filter_cond in enumerate(conds):
            for elem in filter_cond:
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
        return result

    def parse_cte_with_collect(self, attributes, table_aliases_in_query):
        result = ""
        for attribute in attributes:
            if attribute[2] != None:
                self.from_part.add_cte_table_attribute(self.name, attribute[2])
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
        for aggre_fun in CYPHER_AGGREGATING_FUNCTIONS:
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
        limit_string = ""
        if "limit" in self.query.keys():
            limit_string = "[0.." + self.query["limit"].strip() + "]" 
        result += "})" + limit_string + " AS " + self.name + "\n"
        return result + "\n"

    def parse_collected_cte_for_use(self, tables):
        result = ""
        any_of_tables_refering_ctes = False
        for table in tables:
            if table[0] in self.all_cte_names:
                any_of_tables_refering_ctes = True
        if any_of_tables_refering_ctes:
            table_aliases = []
            for table in tables:
                if table[0] in self.all_cte_names:
                    if table[1] != None:
                        result += "UNWIND " + table[0] + " AS " + table[1] + "\n"
                        table_aliases.append(table[1])
                    else:
                        alias = table[0][:3]
                        if "_" in table[0]:
                            res = table[0].split("_")
                            alias = res[0][0] + res[1][0]
                        result += "UNWIND " + table[0] + " AS " + alias + "\n"
                        table_aliases.append(alias)
                else:
                    result += "MATCH (" + table[1] + " : " + table[0] + ")\n"
            if table_aliases != []:
                previous_cte = ""
                for prev_cte in self.previous_ctes:
                    previous_cte += prev_cte + ", "

                for i, elem in enumerate(table_aliases):
                    if i == len(table_aliases) - 1:
                        previous_cte += elem + "\n"
                    else:
                        previous_cte += elem + ", "
                result += "WITH " + previous_cte
        return result

    def parse_joins(self, connections, table_aliases_in_query, join_type):
        result, checked = "", []
        for k, connection in enumerate(connections):
            property1, alias1, key1, property2, alias2, key2 = self.get_property_alias_key_from_connection(connection)
            table_aliases_in_query += [alias1, alias2]
            ## Arrows are pointing from foreign to primary, we need to see which one is which one
            if property1 in self.all_cte_names or property2 in self.all_cte_names:
                for t in range(k, len(connections)):
                    if t not in checked:
                        checked.append(t)
                        connection = connections[t]
                        property1, alias1, key1, property2, alias2, key2 = self.get_property_alias_key_from_connection(connection)
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

    def parse_query_without_connections(self, tables):
        query = ""
        some_table_in_cte = False
        for table in tables:
            if table[0] in self.all_cte_names:
                some_table_in_cte = True
        if some_table_in_cte:
            query += self.parse_collected_cte_for_use(tables)
        else:
            for table in tables:
                if table[1] != None:
                    query += "MATCH (" + table[1] + ":" + table[0] + ")\n"
                else:
                    query += "MATCH (" + table[0] + ")\n"
        return query

    def parse_return_clause(self, select_part):
        result = ""
        for attr in select_part.get_attributes():
            table_name = attr[0]
            if table_name == None:
                table_name = self.from_part.get_cte_table_from_attribute(attr[2])
            if table_name == None:
                result += attr[1] + " AS " + attr[2] + ", "
            if attr[0] != None and attr[2] != None:
                result += table_name + "." + attr[1] + " AS " + attr[2] + ", "
            elif attr[2] == None:
                result += table_name + "." + attr[1] + ", "
        result = result[:-2] + "\n"
        if 'order by' in self.query.keys():
            result += self.query['order by'].get_order_by_cypher() + "\n"
        if 'limit' in self.query.keys():
            result += 'LIMIT ' + self.query['limit']
        return "RETURN " + result

    def get_property_alias_key_from_connection(self, connection):
        alias1, alias2 = connection[0][0].strip(), connection[2][0].strip()
        key1, key2 = connection[0][1].strip(), connection[2][1].strip()
        property1, property2 = self.from_part.get_table_from_alias(alias1), self.from_part.get_table_from_alias(alias2)
        return property1, alias1, key1, property2, alias2, key2