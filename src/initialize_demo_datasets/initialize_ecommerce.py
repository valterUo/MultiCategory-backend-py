from instance_category.objects.collection_object import CollectionObject
from instance_category.morphisms.morphism import Morphism
from instance_category.instance_category import InstanceCategory
from multi_model_join.help_functions import add_to_dict
from functools import reduce
e_commerce_instance = None


def init():
    objects = dict()
    morphisms = dict()

    # Objects in the instance category:

    customers_graph = CollectionObject("customers_graph", "property graph", "customer", lambda graph: list(graph.nodes), {
        "vertex": [
            {"filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\customerVertex.csv", "fileformat": "csv", "schema": ["id", "name", "creditLimit", "locationId"], "keyAttribute": "id"}],
        "edge": [
            {"filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\customerEdge.csv", "fileformat": "csv", "schema": ["source", "target"], "keyAttribute": "source", "fromKeyAttribute": "source", "toKeyAttribute": "target"}]
    })

    interest_graph = CollectionObject("interest_graph", "property graph", "interest", lambda graph: list(graph.nodes), {
        'vertex': [
            {"filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\customerVertex.csv",
                "fileformat": "csv", "schema": ["id", "name", "creditLimit", "locationId"], "keyAttribute": "id"},
            {"filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\interestVertex.csv", "fileformat": "csv", "schema": ["id", "topic", "locationId"], "keyAttribute": "id"}],
        "edge": [
            {"filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\interestEdge.csv", "fileformat": "csv", "schema": ["customerId", "targetId", "weight"], "keyAttribute": "customerId",
             "fromKeyAttribute": "customerId", "toKeyAttribute": "targetId"}]})

    locations_table = CollectionObject("locations_table", "relational", "location", lambda table: table, {"filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\locationsTable.csv",
                                                                                                   "fileformat": "csv", "schema": ["id", "address", "city", "zipCode", "country"], "keyAttribute": "id", "separator": ";"})

    orders_xml = CollectionObject(
        "orders_xml", "XML", "order", lambda document: document.getroot(), {"filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\orders.xml"})

    order_to_customer_key_value_pairs = CollectionObject(
        "order_to_customer_key_value_pairs", "JSON", "pairs", lambda json: json, {"filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\keyValuePairs.json"})

    sitesTable = CollectionObject("sites", "relational", "site", lambda table: table, {"filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\sites.csv",
                                                                                       "fileformat": "csv", "schema": ["id", "locationId", "name", "year", "description"], "keyAttribute": "id", "separator": ";"})

    # Following objects are results to queries that we want to add to the initial instance category

    products_xml = CollectionObject("products_xml", "XML", "product")

    customers_table = CollectionObject("customers_table", "relational", "customer")

    objects["customers_graph"] = customers_graph
    objects["interest_graph"] = interest_graph
    objects["locations_table"] = locations_table
    objects["orders_xml"] = orders_xml
    objects["order_to_customer_key_value_pairs"] = order_to_customer_key_value_pairs
    objects["sitesTable"] = sitesTable
    objects["products_xml"] = products_xml
    objects["customers_table"] = customers_table

    # Morphisms in the instance category:
    # Example: Because orders_xml -> customers_graph -> locations_table is composable, then orderedBy o located is well-defined
    # function that assigns for each order the location where the ordered customer is. For example, composition = located.compose(knows).

    located = Morphism("located", customers_graph, lambda customer: locations_table.getCollection(
    ).get(dict(customer).get("locationId"), "Key not in the dictonary!"), locations_table, True)

    orderedBy = Morphism("orderedBy", orders_xml, lambda elem:  customers_graph.findFromNodes(
        "id", order_to_customer_key_value_pairs.getCollection().get(elem.findall("Order_no")[0].text)), customers_graph, True)

    knows = Morphism("knows", customers_graph, lambda customer: set(
        customers_graph.getCollection().successors(customer)), customers_graph)

    products = Morphism("products", orders_xml,
                        lambda order: order.findall("Product"), products_xml)

    site_located = Morphism("site_located", sitesTable,
                            lambda site: locations_table.getCollection().get(site.get("locationId")), locations_table, True)

    sites_in_location = Morphism("sites_in_location", locations_table, lambda location: reduce(lambda xs, x: add_to_dict(
        xs, x, sitesTable.getCollection()[x]) if sitesTable.getCollection()[x].get("locationId") == location.get("id") else xs, sitesTable.getCollection(), dict()), sitesTable)

    customers = Morphism("customers", customers_graph,
                         lambda customer: dict(customer), customers_table, True)

    ordered_by_customer = Morphism("ordered_by_customer", orders_xml, lambda elem: customers_table.findFromList(
        "id", order_to_customer_key_value_pairs.getCollection().get(elem.findall("Order_no")[0].text)), customers_table, True)

    morphisms["located"] = located
    morphisms["orderedBy"] = orderedBy
    morphisms["knows"] = knows
    morphisms["products"] = products
    morphisms["site_located"] = site_located
    morphisms["sites_in_location"] = sites_in_location
    morphisms["customers"] = customers
    morphisms["ordered_by_customer"] = ordered_by_customer

    global e_commerce_instance

    e_commerce_instance = InstanceCategory("e-commerce", objects, morphisms)
