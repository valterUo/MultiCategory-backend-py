from model_transformations.query_transformations.parse_tree_trasformations.column import Column
from model_transformations.query_transformations.parse_tree_trasformations.where import Where
from external_database_connections.postgresql.postgres import Postgres
from external_database_connections.neo4j.neo4j import Neo4j
rel_db = Postgres("ldbcsf1")
graph_db = Neo4j("ldbcsf1")

class BooleanExpression:

    """
    Postgres source code:

    typedef enum BoolExprType
        {
            AND_EXPR, 
            OR_EXPR, 
            NOT_EXPR
        } BoolExprType;

    Which means that boolop 0 -> AND, boolop 1 -> OR and boolop 2 -> NOT

    """

    def __init__(self, raw_expr, from_clause, cte=False, cte_name = ""):
        self.raw_expr = raw_expr
        self.sources = []
        self.from_clause = from_clause
        self.cte = cte
        self.cte_name = cte_name
        self.boolop = self.raw_expr["boolop"]
        self.mapped_boolop = None

        self.joins = []
        self.possible_joins = []
        self.filters = []

        if self.boolop == 0:
            self.mapped_boolop = "AND"
        elif self.boolop == 1:
            self.mapped_boolop = "OR"
        elif self.boolop == 2:
            self.mapped_boolop = "NOT"


        # First possible join conditions are extracted from the boolean expression
        # Those joins that cannot be transformed into pattern match are appended to filter conditions

        for elem in self.raw_expr["args"]:
            if "A_Expr" in elem.keys():

                left_side = elem["A_Expr"]["lexpr"]
                right_side = elem["A_Expr"]["rexpr"]
                operator = elem["A_Expr"]["name"][0]["String"]["str"]

                if "ColumnRef" in left_side.keys() and "ColumnRef" in right_side.keys():

                    left = Column(
                        left_side["ColumnRef"], self.from_clause, self.cte, self.cte_name)
                    right = Column(
                        right_side["ColumnRef"], self.from_clause, self.cte, self.cte_name)

                    left_table = left.get_collection()
                    right_table = right.get_collection()

                    if left_table and right_table:
                        if rel_db.contains_table(left_table) and rel_db.contains_table(right_table) and operator == "=":
                            self.possible_joins.append((left, right))

                            #join_accepted = self.from_clause.add_join(left, right)

                            #if not join_accepted:
                            #    self.filters.append(elem)
                        else:
                            self.filters.append(elem)
                    else:
                        self.filters.append(elem)
            else:
                self.filters.append(elem)

        
        """
        It is not a trivial task to check if a collection of equalities given in the where clause defines a graph pattern.
        This part relies on certain assumptions in the underlaying data transformation.
        But nothing guarantees that the data transformation follows those assumptions and it does not need to follow them.
        """

        for possible_join in self.possible_joins:
            edge_types = graph_db.get_edge_types()
            left = possible_join[0]
            right = possible_join[1]
            fk = left.get_field()
            pk = right.get_field()


        

        # Analyze those conditions that do not define graph patterns

        for elem in self.filters:
            if "BoolExpr" in elem.keys():
                self.sources.append(BooleanExpression(
                    elem["BoolExpr"], self.from_clause, self.cte, self.cte_name))
            elif "A_Expr" in elem.keys():
                self.sources.append(
                    Where(elem, self.from_clause, self.cte, self.cte_name))
            elif "NullTest" in elem.keys():
                self.sources.append(Where(elem, self.from_clause, self.cte, self.cte_name))

    def transform_into_cypher(self, add_where = True):
        res = ""
        if add_where:
            res = "WHERE "
        for i, elem in enumerate(self.sources):
            if i == len(self.sources) - 1:
                res += elem.transform_into_cypher(False)
            else:
                res += elem.transform_into_cypher(False) + self.mapped_boolop + " "
        return res
