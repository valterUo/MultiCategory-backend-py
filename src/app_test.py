from external_database_connections.neo4j.neo4j import Neo4j


graph_db = Neo4j("ldbcsf1")
graph_query = 'MATCH p=(n)-[r:k_person2id_k_person1id]->(m) WHERE n.p_firstname = "Carmen" AND n.p_lastname = "Lepland" WITH collect(p) as objects RETURN objects LIMIT 25'
res = graph_db.execute_read(graph_query)

with open("C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\src\\test_results\\data_transformations\\rel_to_graph\\person_knows_person.pyc") as file:
    pass