from model_transformations.query_transformations.parse_tree_trasformations.alias_mapping import get_alias_for_name
from model_transformations.query_transformations.parse_tree_trasformations.cte_column_mapping import column_names_to_cte_names_mapping


class Recursive:

    """
    UNWIND cposts AS c
    WITH collect({postid : m.m_messageid, replyof : m.m_c_replyof, orig_postid : m.m_messageid, creator : m.m_creatorid})

    MATCH (m : message)
    UNWIND parent AS p
    WHERE m.m_messageid = p.replyof
    WITH collect({postid : m.m_messageid, replyof : m.m_c_replyof, orig_postid : p.orig_postid, creator : m.m_creatorid}) AS parent

    === recursive part ===

        UNWIND cposts AS c
        MATCH (initial) -[*:m_c_replyof_m_messageid]-> (m : message)
        WHERE initial.m_messageid = c.m_messageid
        WITH collect({ postid : m.m_messageid, replyof : m.m_c_replyof, orig_postid : c.m_messageid, creator : m.m_creatorid }) as parent

    """

    def __init__(self, left_stmt, right_stmt):
        self.left_stmt = left_stmt
        self.right_stmt = right_stmt

    def transform_into_cypher(self):
        res = ""
        
        # Left statement (before UNION) defines the initial state of the recursion
        
        res += self.left_stmt.get_from_clause().transform_into_cypher()
        

        
        # Right statement (after UNION) defines the path pattern and the final return values
        # The assumption is that there is just one edge property that forms the path
        # This edge property is defined by WHERE clause which is mandatory in recursive SQL
        # The initial nodes are taken from the left side (statement before union) and then matched 
        # against the database
        # Also, assumption is that WHERE clause do not include a boolean expression and it needs 
        # to refer to the recursive tables
        # Besides, recursive SQL has a table name that is used to refer to the intermediate results during recursion
        # Neo4j does not need this. That is why we only need to map the intermediate table name to the initial table name
        # so that the references stay correct way.

        where_clause_left = self.right_stmt.get_where_clause().get_where().get_left()
        where_clause_right = self.right_stmt.get_where_clause().get_where().get_right()

        initial_field = None
        
        resursive_alias = self.left_stmt.get_from_clause().get_aliases_not_in_database()[0]
        recursive_field = None
        intermediate_alias = None

        try:
            intermediate_table = column_names_to_cte_names_mapping(where_clause_left.get_field())
            intermediate_alias = get_alias_for_name(intermediate_table)
            initial_field = where_clause_right.get_field()
            recursive_field = where_clause_left.get_field()
        except:
            print("Left side does not refer to the recursive part.")

        try:
            intermediate_table = column_names_to_cte_names_mapping(where_clause_right.get_field())
            intermediate_alias = get_alias_for_name(intermediate_table)
            initial_field = where_clause_left.get_field()
            recursive_field = where_clause_right.get_field()
        except:
            print("Right side does not refer to the recursive part.")

        source = self.right_stmt.get_from_clause().get_from_clause_sources()[0]
        res += "MATCH (initial) - [*] -> " + source.transform_into_cypher() + "\n"
        res += "WHERE initial." + initial_field + "=" + resursive_alias + "." + recursive_field + "\n"
        res += self.right_stmt.get_target_list().transform_into_cypher({intermediate_alias : resursive_alias}) + "\n"

        return res