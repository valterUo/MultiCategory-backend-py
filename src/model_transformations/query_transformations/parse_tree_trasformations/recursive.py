class Recursive:

    """
    Left statement (before UNION) defines the initial state of the recursion
    
    Right statement (after UNION) defines the path pattern and the final return values
    The assumption is that there is just one edge property that forms the path
    This edge property is defined by WHERE clause which is mandatory in recursive SQL
    The initial nodes are taken from the left side (statement before union) and then matched
    against the database
    Also, assumption is that WHERE clause do not include a boolean expression and it needs
    to refer to the recursive tables
    Besides, recursive SQL has a table name that is used to refer to the intermediate results during recursion
    Neo4j does not need this. That is why we only need to map the intermediate table name to the initial table name
    so that the references stay correct way.

    """

    def __init__(self, left_stmt, right_stmt, cte = False, cte_name = ""):
        self.left_stmt = left_stmt
        self.right_stmt = right_stmt
        self.cte = cte
        self.cte_name = cte_name

    def transform_into_cypher(self):
        res = ""
        res += self.left_stmt.get_from_clause().transform_into_cypher()

        where_clause_left = self.right_stmt.get_where_clause().get_where().get_left()
        where_clause_right = self.right_stmt.get_where_clause().get_where().get_right()

        initial_field = None

        resursive_alias = self.left_stmt.get_from_clause(
        ).get_aliases_not_in_database()[0]

        recursive_field = None

        try:
            initial_field = where_clause_right.get_field()
            recursive_field = where_clause_left.get_field()
        except:
            print("Left side does not refer to the recursive part.")

        try:
            initial_field = where_clause_left.get_field()
            recursive_field = where_clause_right.get_field()
        except:
            print("Right side does not refer to the recursive part.")

        source = self.right_stmt.get_from_clause().get_from_clause_sources()[0]
        res += "MATCH (initial) - [*] -> " + \
            source.transform_into_cypher() + "\n"
        res += "WHERE initial." + initial_field + " = " + \
            resursive_alias + "." + recursive_field + "\n"
        res += self.right_stmt.get_target_list().transform_into_cypher()

        if self.cte:
            res += " AS " + self.cte_name + "\n"
        else:
            res += "\n"

        return res
