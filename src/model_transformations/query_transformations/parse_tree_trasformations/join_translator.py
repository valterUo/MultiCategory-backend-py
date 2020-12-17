class JoinTranslator:

    def __init__(self, data_transformation_functor="default"):
        self.functor = data_transformation_functor
        self.joins = []

    def add_join(self, left, right):
        self.joins.append((left, right))

    def get_joins(self):
        return self.joins

    def transform_in_cypher(self):
        res = ""
        for elem in self.joins:
            left = elem[0]
            right = elem[1]
            res += "MATCH (" + left.get_collection_alias() + " : " + left.get_collection() + ")-[" + left.get_field(
            ) + "_" + right.get_field() + "]->(" + right.get_collection_alias() + " : " + right.get_collection() + ")\n"
        return res

    def node_in_join_patterns(self, node):
        for elem in self.joins:
            left = elem[0]
            right = elem[1]
            if left.get_collection_alias() == node.get_rel_alias():
                return True
            if right.get_collection_alias() == node.get_rel_alias():
                return True
        return False
