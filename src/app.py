from SchemaCategory.Objects.NestedDatatype import NestedDatatype
from SchemaCategory.Objects.PrimitiveDatatype import PrimitiveDatatype
from SchemaCategory.Morphisms.Morphism import Morphism
from SchemaCategory.SchemaCategory import SchemaCategory
from DataParsers.CSVParser import *
from DataParsers.PropertyGraphParser import parseDirectedGraph
from DataParsers.XMLParser import *
from InstanceCategory.Objects.CollectionObject import CollectionObject
from DataParsers.RDFParser import *

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

#readToTable("C:\\Users\\Valter Uotila\\Desktop\\demo-system-backend-Haskell\\MultiCategory\\demoData\\locationsTable.csv", ";", ["id", "address", "city", "zipCode", "country"], "id")

# graph = parseDirectedGraph("C:\\Users\\Valter Uotila\\Desktop\\demo-system-backend-Haskell\\MultiCategory\\demoData\\customerVertex.csv",
# "C:\\Users\\Valter Uotila\\Desktop\\demo-system-backend-Haskell\\MultiCategory\\demoData\\customerEdge.csv", ";", ";", ["id", "name", "creditLimit", "locationId"], ["source", "target"], 
# "id", "source", "source", "target")
# print(graph.number_of_nodes())

# graphObject = CollectionObject(["C:\\Users\\Valter Uotila\\Desktop\\demo-system-backend-Haskell\\MultiCategory\\demoData\\customerVertex.csv",
# "C:\\Users\\Valter Uotila\\Desktop\\demo-system-backend-Haskell\\MultiCategory\\demoData\\customerEdge.csv"], "csv", "property graph", "customers", ["id", "name", "creditLimit", "locationId"], "id", ";", ["source", "target"], "source", "source", "target")
# tableObject = CollectionObject("C:\\Users\\Valter Uotila\\Desktop\\demo-system-backend-Haskell\\MultiCategory\\demoData\\locationsTable.csv", "csv", "relational", "locations", ["id", "address", "city", "zipCode", "country"], "id")
# xmlObject = CollectionObject("C:\\Users\\Valter Uotila\\Desktop\\demo-system-backend-Haskell\\MultiCategory\\demoData\\orders.xml", "xml", "XML", "orders")

# printTree(xmlObject.getCollection())

# print(graphObject, tableObject, xmlObject)

rdf = RDFParser("http://www.w3.org/People/Berners-Lee/card")

rdf.printRDF()

