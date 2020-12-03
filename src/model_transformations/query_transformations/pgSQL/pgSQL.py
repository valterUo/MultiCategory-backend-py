import requests
import json

class pgSQL:

    """
    This is unusual setup. SQL parser uses the original Postgres query parser which is extracted from
    the database and implemented in pglast package using Python.

    Pglast cannot be run on Windows which is solved so that there is a small python program running an endpoint where
    parsed queries are sent and the parse tree is retrieved from the parser.

    If we run this program on Linux, we can just install pglast with the normal installation and use it as any package.
    """

    def __init__(self, query_string):
        self.query_string = query_string
        self.parse_tree = None
        try:
            queryload = { "query": self.query_string }
            res = requests.post("http://localhost:5000/sql", data = queryload)
            if res.status_code == 200:
                self.parse_tree = res.json()
                #print(json.dumps(self.parse_tree, indent= 2))
            elif res.status_code == 400:
                print(res.content)
            else:
                print("Unknown error")
        except ConnectionError:
            print("Psql parser is not running in the address 0.0.0.0/5000")
    
    def get_parse_tree(self):
        return self.parse_tree

        