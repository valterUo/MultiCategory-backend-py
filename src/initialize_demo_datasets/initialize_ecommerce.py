from instance_category.objects.collection_object import CollectionObject
from instance_category.morphisms.morphism import Morphism
from instance_category.instance_category import InstanceCategory
from multi_model_join.help_functions import add_to_dict
from functools import reduce
import os
dirname = os.path.dirname(__file__)
e_commerce_instance = None


def init():
    objects = dict()
    morphisms = dict()

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

    # Objects in the instance category:

    customers_graph = CollectionObject("customers_graph", "property graph", "customer", lambda graph: list(graph.nodes), {
        "vertex": [
            {"filePath": customers_vertex_path, "fileformat": "csv", "schema": ["id", "name", "creditLimit", "locationId"], "keyAttribute": "id"}],
        "edge": [
            {"filePath": customers_edge_path, "fileformat": "csv", "schema": ["source", "target"], "keyAttribute": "source", "fromKeyAttribute": "source", "toKeyAttribute": "target"}]
    })

    interest_graph = CollectionObject("interest_graph", "property graph", "interest", lambda graph: list(graph.nodes), {
        'vertex': [
            {"filePath": customers_vertex_path,
                "fileformat": "csv", "schema": ["id", "name", "creditLimit", "locationId"], "keyAttribute": "id"},
            {"filePath": interest_vertex_path, "fileformat": "csv", "schema": ["id", "topic", "locationId"], "keyAttribute": "id"}],
        "edge": [
            {"filePath": interest_edge_path, "fileformat": "csv", "schema": ["customerId", "targetId", "weight"], "keyAttribute": "customerId",
             "fromKeyAttribute": "customerId", "toKeyAttribute": "targetId"}]})

    locations_table = CollectionObject("locations_table", "relational", "location", lambda table: table, {"filePath": locations_table_path, "fileformat": "csv", "schema": ["id", "address", "city", "zipCode", "country"], "keyAttribute": "id", "separator": ";"})

    orders_xml = CollectionObject(
        "orders_xml", "XML", "order", lambda document: document.getroot(), {"filePath": orders_xml_path})

    order_to_customer_key_value_pairs = CollectionObject(
        "order_to_customer_key_value_pairs", "JSON", "pairs", lambda json: json, {"filePath": os.path.join(dirname, "..\\..\\data\\eCommerce\\keyValuePairs.json")})

    sites_table = CollectionObject("sites_table", "relational", "site", lambda table: table, {"filePath": os.path.join(dirname, "..\\..\\data\\eCommerce\\sites.csv"),
                                                                                       "fileformat": "csv", "schema": ["id", "locationId", "name", "year", "description"], "keyAttribute": "id", "separator": ";"})

    # Following objects are results to queries that we want to add to the initial instance category

    products_xml = CollectionObject("products_xml", "XML", "product")

    customers_table = CollectionObject("customers_table", "relational", "customer")

    objects["customers_graph"] = customers_graph
    objects["interest_graph"] = interest_graph
    objects["locations_table"] = locations_table
    objects["orders_xml"] = orders_xml
    objects["order_to_customer_key_value_pairs"] = order_to_customer_key_value_pairs
    objects["sites_table"] = sites_table
    objects["products_xml"] = products_xml
    objects["customers_table"] = customers_table

    # Morphisms in the instance category:
    # Example: Because orders_xml -> customers_graph -> locations_table is composable, then ordered_by o located is well-defined
    # function that assigns for each order the location where the ordered customer is. For example, composition = located.compose(knows).

    located = Morphism("located", customers_graph, lambda customer: locations_table.getCollection(
    ).get(dict(customer).get("locationId"), "Key not in the dictonary!"), locations_table, True)

    ordered_by = Morphism("ordered_by", orders_xml, lambda elem:  customers_graph.findFromNodes(
        "id", order_to_customer_key_value_pairs.getCollection().get(elem.findall("Order_no")[0].text)), customers_graph, True)

    knows = Morphism("knows", customers_graph, lambda customer: set(
        customers_graph.getCollection().successors(customer)), customers_graph)

    products = Morphism("products", orders_xml,
                        lambda order: order.findall("Product"), products_xml)

    site_located = Morphism("site_located", sites_table,
                            lambda site: locations_table.getCollection().get(site.get("locationId")), locations_table, True)

    sites_in_location = Morphism("sites_in_location", locations_table, lambda location: reduce(lambda xs, x: add_to_dict(
        xs, x, sites_table.getCollection()[x]) if sites_table.getCollection()[x].get("locationId") == location.get("id") else xs, sites_table.getCollection(), dict()), sites_table)

    customers = Morphism("customers", customers_graph,
                         lambda customer: dict(customer), customers_table, True)

    ordered_by_customer = Morphism("ordered_by_customer", orders_xml, lambda elem: customers_table.findFromList(
        "id", order_to_customer_key_value_pairs.getCollection().get(elem.findall("Order_no")[0].text)), customers_table, True)

    def findFromOrders(customer):
        result = []
        for elem in orders_xml.getCollection().getroot():
            if order_to_customer_key_value_pairs.getCollection().get(elem.findall("Order_no")[0].text) == int(customer.get("id")):
                result.append(elem)
        return result

    customer_ordered = Morphism(
            "customer_ordered", customers_table, lambda customer: findFromOrders(customer), orders_xml)

    morphisms["located"] = located
    morphisms["ordered_by"] = ordered_by
    morphisms["knows"] = knows
    morphisms["products"] = products
    morphisms["site_located"] = site_located
    morphisms["sites_in_location"] = sites_in_location
    morphisms["customers"] = customers
    morphisms["ordered_by_customer"] = ordered_by_customer
    morphisms["customer_ordered"] = customer_ordered

    global e_commerce_instance

    e_commerce_instance = InstanceCategory("e-commerce", objects, morphisms)
