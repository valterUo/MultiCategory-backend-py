from model_transformations.query_transformations.parse_tree_trasformations.cte_table_data import set_iterator_variable_to_cte, get_cte_iterator_for_cte_name
from model_transformations.query_transformations.parse_tree_trasformations.join_condition import JoinCondition
from model_transformations.query_transformations.parse_tree_trasformations.select_stmt import SelectStmt


class Join:

    """

    Some interesting aspects from Postgres source code:

     typedef enum JoinType
    {
        /*
        * The canonical kinds of joins according to the SQL JOIN syntax. Only
        * these codes can appear in parser output (e.g., JoinExpr nodes).
        */
        JOIN_INNER,                 /* matching tuple pairs only */
        JOIN_LEFT,                  /* pairs + unmatched LHS tuples */
        JOIN_FULL,                  /* pairs + unmatched LHS + unmatched RHS */
        JOIN_RIGHT,                 /* pairs + unmatched RHS tuples */
    
        /*
        * Semijoins and anti-semijoins (as defined in relational theory) do not
        * appear in the SQL JOIN syntax, but there are standard idioms for
        * representing them (e.g., using EXISTS).  The planner recognizes these
        * cases and converts them to joins.  So the planner and executor must
        * support these codes.  NOTE: in JOIN_SEMI output, it is unspecified
        * which matching RHS row is joined to.  In JOIN_ANTI output, the row is
        * guaranteed to be null-extended.
        */
        JOIN_SEMI,                  /* 1 copy of each LHS row that has match(es) */
        JOIN_ANTI,                  /* 1 copy of each LHS row that has no match */
    
        /*
        * These codes are used internally in the planner, but are not supported
        * by the executor (nor, indeed, by most of the planner).
        */
        JOIN_UNIQUE_OUTER,          /* LHS path must be made unique */
        JOIN_UNIQUE_INNER           /* RHS path must be made unique */
    
        /*
        * We might need additional join types someday.
        */
    } JoinType;

    /*
    * OUTER joins are those for which pushed-down quals must behave differently
    * from the join's own quals.  This is in fact everything except INNER and
    * SEMI joins.  However, this macro must also exclude the JOIN_UNIQUE symbols
    * since those are temporary proxies for what will eventually be an INNER
    * join.
    *
    * Note: semijoins are a hybrid case, but we choose to treat them as not
    * being outer joins.  This is okay principally because the SQL syntax makes
    * it impossible to have a pushed-down qual that refers to the inner relation
    * of a semijoin; so there is no strong need to distinguish join quals from
    * pushed-down quals.  This is convenient because for almost all purposes,
    * quals attached to a semijoin can be treated the same as innerjoin quals.
    */
    #define IS_OUTER_JOIN(jointype) \
        (((1 << (jointype)) & \
        ((1 << JOIN_LEFT) | \
            (1 << JOIN_FULL) | \
            (1 << JOIN_RIGHT) | \
            (1 << JOIN_ANTI))) != 0)

    ==============================================================================

    We see that the parse tree numbering follows the rule:
    JOIN_INNER -> 0, JOIN_LEFT -> 1, JOIN_FULL -> 2, JOIN_RIGHT -> 3, 
    JOIN_SEMI -> 4, JOIN_ANTI -> 5, JOIN_UNIQUE_OUTER -> 6, JOIN_UNIQUE_INNER -> 7

    """

    def __init__(self, raw_join, cte=False):
        self.raw_join = raw_join
        self.cte = cte
        self.join_type_int = self.raw_join["jointype"]
        self.join_type = None

        self.left_alias = None
        self.left_content = None

        self.right_alias = None
        self.right_content = None

        if self.join_type_int == 0:
            self.join_type = "JOIN_INNER"
        elif self.join_type_int == 1:
            self.join_type = "JOIN_LEFT"
        elif self.join_type_int == 2:
            self.join_type = "JOIN_FULL"
        elif self.join_type_int == 3:
            self.join_type = "JOIN_RIGHT"
        elif self.join_type_int == 4:
            self.join_type = "JOIN_SEMI"
        elif self.join_type_int == 5:
            self.join_type = "JOIN_ANTI"
        elif self.join_type_int == 6:
            self.join_type = "JOIN_UNIQUE_OUTER"
        elif self.join_type_int == 7:
            self.join_type = "JOIN_UNIQUE_INNER"

        if "RangeSubselect" in self.raw_join["larg"]:
            self.left_alias = self.raw_join["larg"]["RangeSubselect"]["alias"]["Alias"]["aliasname"]
            set_iterator_variable_to_cte(self.left_alias)
            self.left_content = SelectStmt(
                self.raw_join["larg"]["RangeSubselect"]["subquery"]["SelectStmt"], self.left_alias, True)

        if "RangeSubselect" in self.raw_join["rarg"]:
            self.right_alias = self.raw_join["rarg"]["RangeSubselect"]["alias"]["Alias"]["aliasname"]
            set_iterator_variable_to_cte(self.right_alias)
            self.right_content = SelectStmt(
                self.raw_join["rarg"]["RangeSubselect"]["subquery"]["SelectStmt"], self.right_alias, True)

        self.join_condition = JoinCondition(self.raw_join["quals"], self.left_alias, self.right_alias)

    def transform_into_cypher(self):
        res = ""
        if "RangeSubselect" in self.raw_join["larg"] and "RangeSubselect" in self.raw_join["rarg"]:
            res += self.left_content.transform_into_cypher(
            )[0:-1] + "\n\n"
            res += self.right_content.transform_into_cypher(
            )[0:-1] + "\n"
            res += "UNWIND " + self.left_alias + " AS " + get_cte_iterator_for_cte_name(
                self.left_alias) + ", " + self.right_alias + " AS " + get_cte_iterator_for_cte_name(self.right_alias) + "\n"
            res += "WHERE " + self.join_condition.transform_into_cypher() + "\n"
        return res + "\n"
