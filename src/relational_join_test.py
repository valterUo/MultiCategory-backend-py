import unittest
from functools import reduce
import json
from instance_category.objects.collection_object import CollectionObject
from multi_model_join.relational_join import join_relational_relational_over_functional_morphism, join_relational_relational_over_nonfunctional_morphism, join_relational_xml
from instance_category.morphisms.morphism import Morphism
from multi_model_join.help_functions import add_to_dict

customersGraph = CollectionObject("customers", "property graph", "customer", lambda graph : list(graph.nodes), {
    "vertex": [
        {"filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\customerVertex.csv", "fileformat": "csv", "schema": ["id", "name", "creditLimit", "locationId"], "keyAttribute": "id" }],
    "edge": [
            {"filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\customerEdge.csv", "fileformat": "csv", "schema": ["source", "target"], "keyAttribute": "source", "fromKeyAttribute": "source", "toKeyAttribute": "target"}]
})

locationsTable = CollectionObject("locations", "relational", "location", lambda table: table, {"filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\locationsTable.csv",
                                                                                                "fileformat": "csv", "schema": ["id", "address", "city", "zipCode", "country"], "keyAttribute": "id", "separator": ";"})

sitesTable = CollectionObject("sites", "relational", "site", lambda table: table, {"filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\sites.csv",
                                                                                    "fileformat": "csv", "schema": ["id", "locationId", "name", "year", "description"], "keyAttribute": "id", "separator": ";"})

siteLocated = Morphism("siteLocated", sitesTable,
                        lambda site: locationsTable.getCollection().get(site.get("locationId")), locationsTable, True)

sitesInLocation = Morphism("sitesInLocation", locationsTable, lambda location: reduce(lambda xs, x: add_to_dict(
    xs, x, sitesTable.getCollection()[x]) if sitesTable.getCollection()[x].get("locationId") == location.get("id") else xs, sitesTable.getCollection(), dict()), sitesTable)

orderToCustomerKeyValuePairs = CollectionObject(
    "orderToCustomerKeyValuePairs", "JSON", "pairs", lambda json: json, {"filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\src\\keyValuePairs.json"})

ordersXML = CollectionObject(
    "orders", "XML", "order", lambda document: document.getroot(), {"filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\eCommerce\\orders.xml"})

customersTable = CollectionObject("customersTable", "relational", "customer")

customers = Morphism("customers", customersGraph, lambda customer: dict(customer), customersTable, True)

class TestRelationalJoin(unittest.TestCase):

    def findFromOrders(self, customer):
        result = []
        for elem in ordersXML.getCollection().getroot():
            if orderToCustomerKeyValuePairs.getCollection().get(elem.findall("Order_no")[0].text) == int(customer.get("id")):
                result.append(elem)
        return result

    def test_relational_join_xml_twig1(self):
        customerOrdered = Morphism(
            "customerOrdered", customersTable, lambda customer: self.findFromOrders(customer), ordersXML)
        join_result = join_relational_xml(customersTable, customerOrdered, ordersXML, [
                                          "name", "locationId", "Order_no"])
        with open('relational_test_result.json', 'r') as openfile: 
            result_file = json.load(openfile)
        result = result_file[0].get("result")
        self.assertEqual(result, str(join_result.getCollection()))


    def test_relational_join_relational_functional(self):
        with open('relational_test_result.json', 'r') as openfile: 
            result_file = json.load(openfile)
        result = result_file[1].get("result")
        joined_tables = join_relational_relational_over_functional_morphism(
            sitesTable, siteLocated, locationsTable)
        self.assertEqual(result, str(joined_tables.getCollection()))


    def test_relational_join_relational_nonfunctional(self):
        with open('relational_test_result.json', 'r') as openfile: 
            result_file = json.load(openfile)
        result = result_file[2].get("result")
        joined_tables = join_relational_relational_over_nonfunctional_morphism(
            locationsTable, sitesInLocation, sitesTable)
        self.assertEqual(result, str(joined_tables.getCollection()))

if __name__ == '__main__':
    unittest.main()
