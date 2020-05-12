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
from MultiModelJoin.Join import join, add_to_dict
import networkx as nx
import matplotlib.pyplot as plt

customersGraph = CollectionObject("customers", "property graph", {
    "vertex": [
        {"filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\customerVertex.csv", "fileformat": "csv", "schema": ["id", "name", "creditLimit", "locationId"], "keyAttribute": "id" }],
    "edge": [
            {"filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\customerEdge.csv", "fileformat": "csv", "schema": ["source", "target"], "keyAttribute": "source", "fromKeyAttribute": "source", "toKeyAttribute": "target"}]
})

interestGraph = CollectionObject("interests", "property graph", {
    'vertex': [
        {"filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\customerVertex.csv", "fileformat": "csv", "schema": ["id", "name", "creditLimit", "locationId"], "keyAttribute": "id" },
        {"filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\interestVertex.csv", "fileformat": "csv", "schema": ["id", "topic", "locationId"], "keyAttribute": "id"}], 
    "edge": [
        {"filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\interestEdge.csv", "fileformat": "csv", "schema":["customerId", "targetId", "weight"], "keyAttribute": "customerId",
        "fromKeyAttribute": "customerId", "toKeyAttribute": "targetId"}]})

locationsTable = CollectionObject("locations", "relational", { "filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\locationsTable.csv",
                                  "fileformat": "csv", "schema": ["id", "address", "city", "zipCode", "country"], "keyAttribute": "id", "separator": ";" })

ordersXML = CollectionObject(
    "orders", "XML", {"filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\orders.xml"})

orderToCustomerKeyValuePairs = CollectionObject(
    "orderToCustomerKeyValuePairs", "JSON", {"filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\src\\keyValuePairs.json" })

sitesTable = CollectionObject("sites", "relational", {"filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\sites.csv",
                             "fileformat": "csv", "schema": ["id", "locationId", "name", "year", "description"], "keyAttribute": "id", "separator": ";"})

# Because ordersXML -> customersGraph -> locationsTable is composable, then orderedBy o located is well-defined function that assigns for each order the location where the ordered customer is.
located = Morphism("located", customersGraph, lambda customer: locationsTable.getCollection(
).get(dict(customer).get("locationId"), "Key not in the dictonary!"), locationsTable, True)

orderedBy = Morphism("orderedBy", ordersXML, lambda elem:  customersGraph.findFromNodes(
    "id", orderToCustomerKeyValuePairs.getCollection().get(elem.findall("Order_no")[0].text)), customersGraph, True)

knows = Morphism("knows", customersGraph, lambda customer: set(
    customersGraph.getCollection().successors(customer)), customersGraph)

# productsXML = CollectionObject("productsXML", "XML")

# products = Morphism("products", ordersXML,
#                    lambda order: order.findall("Product"), productsXML)

siteLocated = Morphism("siteLocated", sitesTable,
                       lambda site: locationsTable.getCollection().get(site.get("locationId")), locationsTable, True)

sitesInLocation = Morphism("sitesInLocation", locationsTable, lambda location: reduce(lambda xs, x: add_to_dict(
    xs, x, sitesTable.getCollection()[x]) if sitesTable.getCollection()[x].get("locationId") == location.get("id") else xs, sitesTable.getCollection(), dict()), sitesTable)

# print(join(sitesTable, siteLocated, locationsTable))

# join(sitesTable, siteLocated, locationsTable)

# print(join(locationsTable, sitesInLocation, sitesTable))

# join(join(locationsTable, sitesInLocation, sitesTable), siteLocated, locationsTable)

# print(ordersXML.getCollection().getroot().findall("Order")[0].findall("Product"))

# print(interestGraph.getCollection().number_of_edges())

# for edge in interestGraph.getCollection().edges():
#     print(type(edge))

# Create graph join where we (customer1) -> (customer2) if customer1 = customer2

#def m1(customer):

plt.subplot(111)
nx.draw(customersGraph.getCollection(), with_labels=False, font_weight='bold')
plt.show()

