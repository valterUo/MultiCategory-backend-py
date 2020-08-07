import os
dirname = os.path.dirname(__file__)
e_commerce_instance = None


def init():

    customers_vertex_path = os.path.join(
        dirname, "..\\..\\data\\eCommerce\\customerVertex.csv")
    customers_edge_path = os.path.join(
        dirname, "..\\..\\data\\eCommerce\\customerEdge.csv")
    interest_vertex_path = os.path.join(
        dirname, "..\\..\\data\\eCommerce\\interestVertex.csv")
    interest_edge_path = os.path.join(
        dirname, "..\\..\\data\\eCommerce\\interestEdge.csv")
    locations_table_path = os.path.join(
        dirname, "..\\..\\data\\eCommerce\\locationsTable.csv")
    orders_xml_path = os.path.join(
        dirname, "..\\..\\data\\eCommerce\\orders.xml")

    global e_commerce_instance

    e_commerce_instance = None
