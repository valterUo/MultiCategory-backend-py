from model_transformations.query_transformations.parse_tree_trasformations.from_clause_source import FromClauseSource


class FromClause:

    def __init__(self, from_clause):
        self.from_clause = from_clause
        self.sources = []
        self.joins = []

        if type(self.from_clause) == list:
            for elem in self.from_clause:
                if "RangeVar" in elem.keys():
                    self.sources.append(FromClauseSource(elem))
                if "JoinExpr" in elem.keys():
                    self.joins.append(elem["JoinExpr"])
    
    def get_sources(self):
        return self.sources

    def transform_into_cypher(self):
        res = ""
        matches = [elem for elem in self.sources if elem.get_if_in_database()]
        unwinds = [elem for elem in self.sources if not elem.get_if_in_database()]
        rel_names_in_joins = []
        # for elem in self.joins:
        #     rel_names_in_joins += elem.get_rel_names()
        if len(matches) > 0:
            res = "MATCH "
            for elem in matches:
                if elem.get_relname() not in rel_names_in_joins:
                    res += elem.transform_into_cypher() + ", "
            res = res[0:-2] + "\n"
        # if len(self.joins) > 0:
        #     for elem in self.joins:
        #         res += "MATCH "
        #         res += elem.transform_into_cypher() + "\n"
        if len(unwinds) > 0:
            res += "UNWIND "
            for elem in unwinds:
                res += elem.transform_into_cypher() + ", "
            res = res[0:-2] + "\n"
        return res

    def append_to_joins(self, join):
        self.joins.append(join)

    def get_from_clause_sources(self):
        return self.sources

    def get_aliases(self):
        return [elem.get_aliasname() for elem in self.sources]

    def get_relnames_not_in_database(self):
        return [elem.get_relname() for elem in self.sources if not elem.get_if_in_database()]

    def get_aliases_not_in_database(self):
        return [elem.get_aliasname() for elem in self.sources if not elem.get_if_in_database()]