import string
import re
import random
from model_transformations.query_language_transformations.SQL.global_variables import KEYWORDS

def remove_comments(query):
    ## Multi-line comments
    multi_line_comment_ex = re.compile(r'(\/\*).*(\*\/)', re.DOTALL)
    result = re.sub(multi_line_comment_ex, '', query)
    ## One line comments
    result = re.sub(r'(--).*(\n|\r|\rn)', '', result)
    return result.strip()

def get_keyword_sequence(query):
    keyword_sequence = list()
    words = re.split(r'\s', query)
    for i in range(len(words) - 1):
        if words[i].strip() in KEYWORDS:
            keyword_sequence.append(words[i].strip())
        elif words[i].strip() + " " + words[i+1].strip() in KEYWORDS:
            keyword_sequence.append(
                words[i].strip() + " " + words[i+1].strip())
    keyword_sequence = list(dict.fromkeys(keyword_sequence))
    return keyword_sequence

def parse_query_with_keywords(keyword_from, query, keyword_to = None):
    start_indexes = [m.start() for m in re.finditer(keyword_from, query)]
    paranthesis = []
    for i, c in enumerate(query):
        if c == "(":
            paranthesis.append("(")
        elif c == ")":
            if len(paranthesis) == 0:
                break
            else:
                paranthesis.pop()
        if len(paranthesis) > 0:
            for start_i in start_indexes:
                if start_i == i:
                    start_indexes.remove(start_i)
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


def extract_common_table_expressions(query):
    ctes = dict()
    collecting, collecting_name, collecting_subquery, collecting_main = False, False, False, False
    name, subquery, main_query, paranthesis = "", "", "", []
    for i in range(len(query)):
        if query[i-4:i] == "with":
            collecting = True
            collecting_name = True
        if collecting_name:
            if query[i:i+2] == "as":
                collecting_name = False
                collecting_subquery = True
            else:
                name += query[i]
        if collecting_subquery:
            subquery += query[i]
            if query[i] == "(":
                paranthesis.append("(")
            if query[i] == ")":
                paranthesis.pop()
                if len(paranthesis) == 0:
                    ctes[name.strip()] = subquery
                    name, subquery = "", ""
                    collecting_subquery = False
        if collecting and not collecting_subquery and not collecting_name and not collecting_main:
            if query[i] == ",":
                collecting_name = True
            else:
                if re.match(r'[a-z]', query[i]) != None:
                    collecting_main = True
        if collecting_main and collecting:
            main_query += query[i]

    if main_query == "":
        ctes["main"] = query
    else:
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