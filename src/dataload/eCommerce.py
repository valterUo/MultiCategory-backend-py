from InstanceCategory.Morphisms.Morphism import Morphism
from InstanceCategory.Objects.CollectionObject import CollectionObject

customersGraph = CollectionObject(["C:\\Users\\Valter Uotila\\Desktop\\demo-system-backend-Haskell\\MultiCategory\\demoData\\customerVertex.csv",
"C:\\Users\\Valter Uotila\\Desktop\\demo-system-backend-Haskell\\MultiCategory\\demoData\\customerEdge.csv"], "csv", "property graph", "customers", ["id", "name", "creditLimit", "locationId"], "id", ";", ["source", "target"], "source", "source", "target")

locationsTable = CollectionObject("C:\\Users\\Valter Uotila\\Desktop\\demo-system-backend-Haskell\\MultiCategory\\demoData\\locationsTable.csv", "csv", "relational", "locations", ["id", "address", "city", "zipCode", "country"], "id")

ordersXML = CollectionObject("C:\\Users\\Valter Uotila\\Desktop\\demo-system-backend-Haskell\\MultiCategory\\demoData\\orders.xml", "xml", "XML", "orders")

orderToCustomerKeyValuePairs = CollectionObject("keyValuePairs.json", "json", "JSON", "orderToCustomerKeyValuePairs")

# Because ordersXML -> customersGraph -> locationsTable is composable, then orderedBy o located is well-defined function that assigns for each order the location where the ordered customer is.
located = Morphism("located", customersGraph, locationsTable, lambda customer : locationsTable.getCollection().get(dict(customer).get("locationId"), "Key not in the dictonary!"), True)

orderedBy = Morphism("orderedBy", ordersXML, customersGraph, lambda elem :  customersGraph.findFromNodes("id", orderToCustomerKeyValuePairs.getCollection().get(elem.findall("Order_no")[0].text)), True)

knows = Morphism("knows", customersGraph, customersGraph, lambda customer : set(customersGraph.getCollection().successors(customer)))

composition = located.compose(knows)

print(composition)

print(composition.getRelation)
for elem in composition.getRelation()(frozenset({('id', '20'), ('locationId', '14'), ('name', 'Charlotte'), ('creditLimit', '789')})):
    print(elem)

composition2 = knows.compose(knows.compose(knows.compose(knows)))

for elem in composition2.getRelation()(frozenset({('id', '20'), ('locationId', '14'), ('name', 'Charlotte'), ('creditLimit', '789')})):
    print(elem)