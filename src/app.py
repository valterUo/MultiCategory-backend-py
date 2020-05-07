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
from MultiModelJoin.Join import *

customersGraph = CollectionObject("customers", "property graph", ["C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\customerVertex.csv",
                                                                  "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\customerEdge.csv"], "csv", ["id", "name", "creditLimit", "locationId"], "id", ";", ["source", "target"], "source", "source", "target")

locationsTable = CollectionObject("locations", "relational", "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\locationsTable.csv",
                                  "csv", ["id", "address", "city", "zipCode", "country"], "id")

ordersXML = CollectionObject(
    "orders", "XML", "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\orders.xml", "xml")

orderToCustomerKeyValuePairs = CollectionObject(
    "orderToCustomerKeyValuePairs", "JSON", "keyValuePairs.json", "json")

sitesTable = CollectionObject("sites", "relational", "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\sites.csv",
                              "csv", ["id", "locationId", "name", "year", "description"], "id")

# Because ordersXML -> customersGraph -> locationsTable is composable, then orderedBy o located is well-defined function that assigns for each order the location where the ordered customer is.
located = Morphism("located", customersGraph, locationsTable, lambda customer: locationsTable.getCollection(
).get(dict(customer).get("locationId"), "Key not in the dictonary!"), True)

orderedBy = Morphism("orderedBy", ordersXML, customersGraph, lambda elem:  customersGraph.findFromNodes(
    "id", orderToCustomerKeyValuePairs.getCollection().get(elem.findall("Order_no")[0].text)), True)

knows = Morphism("knows", customersGraph, customersGraph, lambda customer: set(
    customersGraph.getCollection().successors(customer)))

products = Morphism("products", ordersXML, ordersXML,
                    lambda order: order.findall("Product"))

siteLocated = Morphism("siteLocated", sitesTable, locationsTable,
                       lambda site: locationsTable.getCollection().get(site.get("locationId")), True)

sitesInLocation = Morphism("sitesInLocation", locationsTable, sitesTable, lambda location: reduce(lambda xs, x: add_to_dict(
    xs, x, sitesTable.getCollection()[x]) if sitesTable.getCollection()[x].get("locationId") == location.get("id") else xs, sitesTable.getCollection(), dict()))

print(join(sitesTable, siteLocated, locationsTable))

print(join(locationsTable, sitesInLocation, sitesTable))

