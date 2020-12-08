import string
import random

from model_transformations.query_transformations.parse_tree_trasformations.alias_error import AliasNameError
aliases_to_db_names = dict()
db_names_to_aliases = dict()


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def alias_mapping(name):
    """
    Table or column alias uniquely refers to certain table or column within the certain limits in the query.

    This mapping is 1-1 implementation that holds information about the aliases and table and column names.
    """

    global aliases_to_db_names
    global db_names_to_aliases

    if name in aliases_to_db_names.keys():
        return aliases_to_db_names[name]

    if name in db_names_to_aliases.keys():
        return db_names_to_aliases[name]

    # The program assumes that name is relname and creates an alias for it
    # If there are lots of columns with the same name (very rare), then the alias is randomly selected

    relname = name
    letters = ""

    for c in relname:
        letters += c
        if letters not in aliases_to_db_names.keys():
            aliases_to_db_names[letters] = relname
            db_names_to_aliases[relname] = letters
            return letters
    else:
        while True:
            letters = get_random_string(3)
            if letters not in aliases_to_db_names.keys():
                aliases_to_db_names[letters] = relname
                db_names_to_aliases[relname] = letters
                return letters


def get_alias_for_name(name):
    return alias_mapping(name)

def get_name_for_alias(name):
    return aliases_to_db_names[name]


def set_alias_for_db_name(alias, name):
    global aliases_to_db_names
    global db_names_to_aliases

    if alias in aliases_to_db_names.keys():
        current_name = aliases_to_db_names[alias]
        if current_name != name:
            raise AliasNameError("Alias" + alias + " is already mapped to name " +
                                 current_name + " and cannot be assigned to " + name)
    else:
        aliases_to_db_names[alias] = name
    if name in db_names_to_aliases.keys():
        current_alias = db_names_to_aliases[name]
        if current_alias != alias:
            raise AliasNameError("Name " + name + " is already mapped to alias" +
                                 current_alias + " and cannot be assigned to " + alias)
    else:
        db_names_to_aliases[name] = alias


def reset_aliases():

    global aliases_to_db_names
    global db_names_to_aliases

    aliases_to_db_names = dict()
    db_names_to_aliases = dict()
