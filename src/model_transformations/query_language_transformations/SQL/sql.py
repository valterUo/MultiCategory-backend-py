import re
KEYWORDS = ['select', 'from', 'where', 'inner join', 'outer join', 'left join', 'right join', 'full join', 'group by', 'order by', 'limit']

class SQL:

    def __init__(self, name, query_string):
        self.name = name
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
            for elem in self.query:
                print(elem, self.query[elem])

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
