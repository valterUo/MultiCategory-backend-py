# from external_database_connections.neo4j.neo4j import Neo4j
# graph_db = Neo4j("ldbcsf1")
# graph_query = 'MATCH p=(n)-[r:k_person2id_k_person1id]->(m) WHERE n.p_firstname = "Carmen" AND n.p_lastname = "Lepland" WITH collect(p) as objects RETURN objects LIMIT 25'
# graph_query = 'MATCH p=()-[r:pt_tagid_pt_personid]->() RETURN count(p)'
# res = graph_db.execute_read(graph_query)
# print(res[0]["count(p)"] == 39170)