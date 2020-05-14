from functools import reduce
from SchemaCategory.Objects.NestedDatatype import NestedDatatype
from SchemaCategory.Objects.PrimitiveDatatype import PrimitiveDatatype
from InstanceCategory.Morphisms.Morphism import Morphism
from SchemaCategory.SchemaCategory import SchemaCategory
from DataParsers.CSVParser import *
from DataParsers.PropertyGraphParser import parseDirectedGraph
from DataParsers.XMLParser import *
from InstanceCategory.Objects.CollectionObject import CollectionObject
from DataParsers.RDFParser import *
from MultiModelJoin.Join import add_to_dict, join, join_relational_xml
import networkx as nx
import matplotlib.pyplot as plt

# Objects in the instance category:

customersGraph = CollectionObject("customers", "property graph", "customer", lambda graph : list(graph.nodes), {
    "vertex": [
        {"filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\customerVertex.csv", "fileformat": "csv", "schema": ["id", "name", "creditLimit", "locationId"], "keyAttribute": "id" }],
    "edge": [
            {"filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\customerEdge.csv", "fileformat": "csv", "schema": ["source", "target"], "keyAttribute": "source", "fromKeyAttribute": "source", "toKeyAttribute": "target"}]
})

interestGraph = CollectionObject("interests", "property graph", "interest", lambda graph : list(graph.nodes), {
    'vertex': [
        {"filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\customerVertex.csv", "fileformat": "csv", "schema": ["id", "name", "creditLimit", "locationId"], "keyAttribute": "id" },
        {"filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\interestVertex.csv", "fileformat": "csv", "schema": ["id", "topic", "locationId"], "keyAttribute": "id"}], 
    "edge": [
        {"filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\interestEdge.csv", "fileformat": "csv", "schema":["customerId", "targetId", "weight"], "keyAttribute": "customerId",
        "fromKeyAttribute": "customerId", "toKeyAttribute": "targetId"}]})

locationsTable = CollectionObject("locations", "relational", "location", lambda table : table, { "filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\locationsTable.csv",
                                  "fileformat": "csv", "schema": ["id", "address", "city", "zipCode", "country"], "keyAttribute": "id", "separator": ";" })

ordersXML = CollectionObject(
    "orders", "XML", "order", lambda document : document.getroot(), {"filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\orders.xml"})

orderToCustomerKeyValuePairs = CollectionObject(
    "orderToCustomerKeyValuePairs", "JSON", "pairs", lambda json : json, {"filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\src\\keyValuePairs.json" })

sitesTable = CollectionObject("sites", "relational", "site", lambda table : table, {"filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\sites.csv",
                             "fileformat": "csv", "schema": ["id", "locationId", "name", "year", "description"], "keyAttribute": "id", "separator": ";"})

# Following objects are results to queries

productsXML = CollectionObject("productsXML", "XML", "product")

customersTable = CollectionObject("customersTable", "relational", "customer")

# Morphisms in the instance category:
# Example: Because ordersXML -> customersGraph -> locationsTable is composable, then orderedBy o located is well-defined function that assigns for each order the location where the ordered customer is.

located = Morphism("located", customersGraph, lambda customer: locationsTable.getCollection(
).get(dict(customer).get("locationId"), "Key not in the dictonary!"), locationsTable, True)

orderedBy = Morphism("orderedBy", ordersXML, lambda elem:  customersGraph.findFromNodes(
    "id", orderToCustomerKeyValuePairs.getCollection().get(elem.findall("Order_no")[0].text)), customersGraph, True)

knows = Morphism("knows", customersGraph, lambda customer: set(
    customersGraph.getCollection().successors(customer)), customersGraph)

products = Morphism("products", ordersXML,
                   lambda order: order.findall("Product"), productsXML)

siteLocated = Morphism("siteLocated", sitesTable,
                       lambda site: locationsTable.getCollection().get(site.get("locationId")), locationsTable, True)

sitesInLocation = Morphism("sitesInLocation", locationsTable, lambda location: reduce(lambda xs, x: add_to_dict(
    xs, x, sitesTable.getCollection()[x]) if sitesTable.getCollection()[x].get("locationId") == location.get("id") else xs, sitesTable.getCollection(), dict()), sitesTable)

customers = Morphism("customers", customersGraph, lambda customer: dict(customer), customersTable, True)

orderedByCustomer = Morphism("orderedByCustomer", ordersXML, lambda elem : customersTable.findFromList("id", orderToCustomerKeyValuePairs.getCollection().get(elem.findall("Order_no")[0].text)), customersTable, True)

result = join_relational_xml(customersTable, orderedByCustomer, ordersXML, ["name", "locationId", "Order_no"])