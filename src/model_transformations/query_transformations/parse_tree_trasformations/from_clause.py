from model_transformations.query_transformations.parse_tree_trasformations.from_clause_source import FromClauseSource


class FromClause:

    def __init__(self, from_clause, cte_name):
        self.from_clause = from_clause
        self.cte_name = cte_name
        self.sources = []
        self.joins = []

        if type(self.from_clause) == list:
            for elem in self.from_clause:
                if "RangeVar" in elem.keys():
                    self.sources.append(FromClauseSource(elem, self.cte_name))
                if "JoinExpr" in elem.keys():
                    from model_transformations.query_transformations.parse_tree_trasformations.join import Join
                    self.joins.append(Join(elem["JoinExpr"]))


    def transform_into_cypher(self):
        res = ""
        if self.sources:
            matches = [elem for elem in self.sources if elem.get_if_in_database()]
            unwinds = [elem for elem in self.sources if not elem.get_if_in_database()]

            if len(matches) > 0:
                res = "MATCH "
                for elem in matches:
                    res += elem.transform_into_cypher() + ", "
                res = res[0:-2] + "\n"

            if len(unwinds) > 0:
                res += "UNWIND "
                for elem in unwinds:
                    res += elem.transform_into_cypher() + ", "
                res = res[0:-2] + "\n"
            
            if self.joins:
                for elem in self.joins:
                    res += elem.transform_into_cypher()

        return res

    def get_from_clause_sources(self):
        return self.sources

    def get_aliases(self):
        return [elem.get_rel_alias() for elem in self.sources]

    def get_relnames(self):
        return [elem.get_relname() for elem in self.sources]
        
    def get_relnames_not_in_database(self):
        return [elem.get_relname() for elem in self.sources if not elem.get_if_in_database()]

    def get_aliases_not_in_database(self):
        return [elem.get_rel_alias() for elem in self.sources if not elem.get_if_in_database()]

    def get_alias_for_relname(self, relname):
        for source in self.sources:
            if source.get_relname() == relname:
                return source.get_rel_alias()