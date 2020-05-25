from functools import reduce
import networkx as nx
import json
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from instance_category.objects.collection_object import CollectionObject
from instance_category.morphisms.morphism import Morphism
from multi_model_join.join import add_to_dict, join, join_relational_xml
from multi_model_join.graph_join.graph_join import join_graph_graph
from multi_model_join.relational_join import join_relational_relational_over_functional_morphism
from multi_model_join.relational_join import join_relational_relational_over_nonfunctional_morphism

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

# joined_tables = join_relational_relational_over_functional_morphism(
#             sitesTable, siteLocated, locationsTable)

# joined_tables2 = join_relational_relational_over_nonfunctional_morphism(
#             locationsTable, sitesInLocation, sitesTable)
 
# json_object = json.dumps([{'result': str(joined_tables.getCollection())}, {'result': str(joined_tables2.getCollection())}]) 
  
# with open("relational_test_result.json", "w") as outfile: 
#     outfile.write(json_object)

#print(joined_tables.getCollection())


# gluing_graph = nx.DiGraph()
# elem1 = frozenset({('id', '23'), ('locationId', '11'), ('name', 'David'), ('creditLimit', '1245')})
# elem2 = frozenset({('locationId', '14'), ('id', '17'), ('creditLimit', '21'), ('name', 'Julia')})
# gluing_graph.add_node(0)
# gluing_graph.add_node(1)
# gluing_graph.add_edge(0, 1)
# gluing_graph.nodes[0] = 1
# print(gluing_graph.nodes[0], gluing_graph.nodes[1])

# morphism = [("x", frozenset({('id', '23'), ('locationId', '11'), ('name', 'David'), ('creditLimit', '1245')})),
# ("y", frozenset({('locationId', '14'), ('id', '17'), ('creditLimit', '21'), ('name', 'Julia')}))]

# morphism_induced_by_function = lambda customer1, customer2 : True if dict(customer1).get("creditLimit") > dict(customer2).get("creditLimit") else False

# join_graph = join_graph_graph(customersGraph, morphism_induced_by_function, customersGraph, gluing_graph)

# print(join_graph)

# plt.subplot(111)
# nx.draw(join_graph.getCollection(), with_labels=False, font_weight='bold')
# plt.show()

# gluing_graph = nx.DiGraph()
# gluing_graph.add_node(0)

# customer1 = frozenset({('id', '14'), ('locationId', '15'), ('creditLimit', '2900'), ('name', 'Lucas')})
# customer2 = frozenset({('locationId', '11'), ('name', 'David'), ('id', '23'), ('creditLimit', '1245')})
# customer3 = frozenset({('id', '7'), ('creditLimit', '9999'), ('locationId', '10'), ('name', 'Bob')})
# customer4 = frozenset({('name', 'Hannah'), ('creditLimit', '7458'), ('id', '16'), ('locationId', '16')})

# customerGraph1 = nx.DiGraph()
# customerGraph1.add_edges_from([(customer1, customer2), (customer2, customer3), (customer3, customer4), (customer4, customer1)])

# interest1 = frozenset({('locationId', '13'), ('topic', 'pottery'), ('id', 'I3')})
# interest2 = frozenset({('locationId', '15'), ('topic', 'volunteering'), ('id', 'I5')})
# interest3 = frozenset({('locationId', '16'), ('id', 'I6'), ('topic', 'dancing')})

# customerGraph2 = nx.DiGraph()
# customerGraph2.add_edges_from([(customer1, interest1), (customer2, interest2), (customer1, interest3), (customer2, interest3)])

# instanceObject1 = CollectionObject("customers1", "property graph", "customer", lambda graph : list(graph.nodes), None, customerGraph1)
# instanceObject2 = CollectionObject("customers2", "property graph", "customer", lambda graph : list(graph.nodes), None, customerGraph2)

# morphism_induced_by_function = lambda customer, customer_or_interest : True if customer == customer_or_interest else False

# join_graph = join_graph_graph(instanceObject1, morphism_induced_by_function, instanceObject2, gluing_graph)

# print(join_graph)

# for node in join_graph.getCollection().nodes:
#     print(node)

# print(join_graph.getCollection().nodes())
# plt.subplot(111)
# nx.draw(join_graph.getCollection(), with_labels=False, font_weight='bold')
# plt.show()


def findFromOrders(customer):
    result = []
    for elem in ordersXML.getCollection().getroot():
        if orderToCustomerKeyValuePairs.getCollection().get(elem.findall("Order_no")[0].text) == int(customer.get("id")):
            result.append(elem)
    return result

customerOrdered = Morphism(
    "customerOrdered", customersTable, lambda customer: findFromOrders(customer), ordersXML)

#print(customersTable.getCollection())

join_result = join_relational_xml(customersTable, customerOrdered, ordersXML, [
                                    "name", "locationId", "Order_no", "Product_Name"])

print(join_result.getCollection())