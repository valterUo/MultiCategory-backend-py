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
from MultiModelJoin.Join import join

# nested = NestedDatatype("Person", [], [])
# primitive_name = PrimitiveDatatype("Name", "String", [])
# primitive_age = PrimitiveDatatype("Age", "Int", [])

# name_morphism = Morphism("name", nested, primitive_name)
# age_morphism = Morphism("age", nested, primitive_age)

# nested.add_morphism(name_morphism)
# nested.add_morphism(age_morphism)
# primitive_name.add_morphism(name_morphism)
# primitive_age.add_morphism(age_morphism)

# #print(nested.outGoingMorphisms[0].targetObj.inComingMorphisms)

# schemaCategory = SchemaCategory([nested, primitive_name, primitive_age], [name_morphism, age_morphism])
# #print(schemaCategory)

# readToTable("C:\\Users\\Valter Uotila\\Desktop\\demo-system-backend-Haskell\\MultiCategory\\demoData\\locationsTable.csv", ";", ["id", "address", "city", "zipCode", "country"], "id")

# graph = parseDirectedGraph("C:\\Users\\Valter Uotila\\Desktop\\demo-system-backend-Haskell\\MultiCategory\\demoData\\customerVertex.csv",
# "C:\\Users\\Valter Uotila\\Desktop\\demo-system-backend-Haskell\\MultiCategory\\demoData\\customerEdge.csv", ";", ";", ["id", "name", "creditLimit", "locationId"], ["source", "target"], 
# "id", "source", "source", "target")
# print(graph.number_of_nodes())

# printTree(ordersXML.getCollection())
# print(customersGraph)

# rdf = RDFParser("http://www.w3.org/People/Berners-Lee/card")
# rdf.printRDF()

# fn = lambda c : locationsTable.getCollection().get(dict(c).get("locationId"), "Key not in the dictonary!")
# print(fn(frozenset({('name', 'Mill'), ('id', '6'), ('locationId', '11'), ('creditLimit', '0')})))
# print(ordersXML.getCollection().getroot().findall("Order"))
# for elem in ordersXML.getCollection().getroot().findall("Order"):
#     for elem2 in elem.findall("Order_no"):
#         print(elem2.tag, elem2.text)

# fn = lambda elem :  customersGraph.findFromNodes("id", orderToCustomerKeyValuePairs.getCollection().get(elem.findall("Order_no")[0].text))

# print(customersGraph.findFromNodes("id", orderToCustomerKeyValuePairs.getCollection().get(ordersXML.getCollection().getroot().findall("./Order/Order_no")[0].text)))

customersGraph = CollectionObject("customers", "property graph", ["C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\customerVertex.csv",
"C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\customerEdge.csv"], "csv", ["id", "name", "creditLimit", "locationId"], "id", ";", ["source", "target"], "source", "source", "target")

locationsTable = CollectionObject("locations", "relational", "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\locationsTable.csv", "csv", ["id", "address", "city", "zipCode", "country"], "id")

ordersXML = CollectionObject("orders", "XML", "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\orders.xml", "xml")

orderToCustomerKeyValuePairs = CollectionObject("orderToCustomerKeyValuePairs", "JSON", "keyValuePairs.json", "json")

sitesTable = CollectionObject("sites", "relational", "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\sites.csv", "csv", ["id", "locationId", "name", "year", "description"], "id")

# Because ordersXML -> customersGraph -> locationsTable is composable, then orderedBy o located is well-defined function that assigns for each order the location where the ordered customer is.
located = Morphism("located", customersGraph, locationsTable, lambda customer : locationsTable.getCollection().get(dict(customer).get("locationId"), "Key not in the dictonary!"), True)

orderedBy = Morphism("orderedBy", ordersXML, customersGraph, lambda elem :  customersGraph.findFromNodes("id", orderToCustomerKeyValuePairs.getCollection().get(elem.findall("Order_no")[0].text)), True)

knows = Morphism("knows", customersGraph, customersGraph, lambda customer : set(customersGraph.getCollection().successors(customer)))

products = Morphism("products", ordersXML, ordersXML, lambda order : order.findall("Product"))

siteLocated = Morphism("siteLocated", sitesTable, locationsTable, lambda site : locationsTable.getCollection().get(site.get("locationId")))

# sitesInLocation = Morphism("sitesInLocation", locationsTable, sitesTable, lambda location : reduce(lambda x, xs : xs.add(x) if x.get("locationId") == location.get("id") else xs, sitesTable.getCollection(), set()))

print(join(sitesTable, siteLocated, locationsTable))

# composition = located.compose(knows)

# print(composition)

# print(composition.getRelation)
# for elem in composition.getRelation()(frozenset({('id', '20'), ('locationId', '14'), ('name', 'Charlotte'), ('creditLimit', '789')})):
#     print(elem)

# composition2 = knows.compose(knows.compose(knows.compose(knows)))

# Compose the knows morphism 20 times:
# composition = knows
# for i in range(20):
#     composition = composition.compose(knows)

# for elem in composition.getRelation()(frozenset({('id', '20'), ('locationId', '14'), ('name', 'Charlotte'), ('creditLimit', '789')})):
#     print(elem)
